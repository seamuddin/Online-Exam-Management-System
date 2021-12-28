from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User
from exam import models as QMODEL
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.forms.models import model_to_dict


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'exam/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_teacher(request.user):
        if request.POST:
            verifyno = TMODEL.Teacher.objects.filter(user_id=request.user.id).values('verification')
            verifydata = verifyno[0]['verification']
            if str(request.POST['verifynumber']) == str(verifydata):
                teacherm = TMODEL.Teacher.objects.get(user_id=request.user.id)
                teacherm.verify_state = 1
                teacherm.save()
                accountapproval = TMODEL.Teacher.objects.all().filter(user_id=request.user.id, status=True,)
                if accountapproval:
                    return redirect('teacher/teacher-dashboard')
                else:
                    return render(request, 'teacher/teacher_wait_for_approval.html')
            else:
                return render(request, 'teacher/verify.html')
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True,)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            verify = TMODEL.Teacher.objects.all().filter(user_id=request.user.id, verify_state = 0)
            if verify:
                return render(request, 'teacher/verify.html')
            else:
                return render(request,'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.QCourse.objects.all().count(),
    'total_dept':models.Department.objects.all().count(),
    }
    return render(request,'exam/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'exam/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'exam/update_teacher.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')




@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'exam/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    import pdb; pdb.set_trace()
    teacher = TMODEL.Teacher.objects.get(id=pk)
    teacher.status = True
    teacher.save()
    teachers = TMODEL.Teacher.objects.all().filter(status=False)
    return render(request, 'exam/admin_view_pending_teacher.html', {'teachers': teachers})

@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher_salary.html',{'teachers':teachers})




@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'exam/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student.html',{'students':students})



@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'exam/update_student.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_course_view(request):
    return render(request,'exam/admin_course.html')

@login_required(login_url='adminlogin')
def admin_dept_view(request):
    return render(request,'exam/admin_department.html')

@login_required(login_url='adminlogin')
def admin_cwt_view(request):
    return render(request,'exam/admin_cwt.html')



@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.QCourseForm()
    if request.method=='POST':
        courseForm=forms.QCourseForm(request.POST)
        if courseForm.is_valid():
            course = courseForm.save(commit=False)
            department = QMODEL.Department.objects.get(id=request.POST.get('dept_id'))
            course.course_dept = department
            course.course_dept_name = department.dept_name
            course.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'exam/admin_add_course.html',{'courseForm':courseForm})


@login_required(login_url='adminlogin')
def admin_add_dept_view(request):
    DeptForm=forms.DeptForm()
    if request.method=='POST':
        DeptForm=forms.DeptForm(request.POST)
        if DeptForm.is_valid():
            DeptForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-dept')
    return render(request,'exam/admin_add_dept.html',{'courseForm':DeptForm})


@login_required(login_url='adminlogin')
def admin_add_cwt_view(request):
    CWTForm=forms.CWTForm()
    if request.method=='POST':
        CWTForm=forms.CWTForm(request.POST)
        if CWTForm.is_valid():
            CWT = CWTForm.save(commit=False)
            course = QMODEL.QCourse.objects.get(id=request.POST.get('course_id'))
            teacher = TMODEL.Teacher.objects.get(id=request.POST.get('teacher_id'))
            CWT.course = course
            CWT.teacher = teacher
            CWT.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-cwt')
    return render(request,'exam/admin_add_cwt.html',{'courseForm':CWTForm})



@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.QCourse.objects.all()
    return render(request,'exam/admin_view_course.html',{'courses':courses})


@login_required(login_url='adminlogin')
def admin_view_dept_view(request):
    courses = models.Department.objects.all()
    return render(request,'exam/admin_view_dept.html',{'courses':courses})

@login_required(login_url='adminlogin')
def admin_view_cwt_view(request):
    courses = models.CourseWiseTeacher.objects.all()
    mydict = []
    for i in courses:
        course_dict = i.__dict__
        course = models.QCourse.objects.filter(id = course_dict.get('course_id')).values_list('course_name', 'course_code')
        course_dict.update({'course_name':course[0][0],'teacher_name':i.teacher})
        mydict.append(course_dict)
    return render(request,'exam/admin_view_cwt.html',{'courses':mydict})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=models.QCourse.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')




@login_required(login_url='adminlogin')
def delete_dept_view(request,pk):
    dept=models.Department.objects.get(id=pk)
    dept.delete()
    return HttpResponseRedirect('/admin-view-dept')

@login_required(login_url='adminlogin')
def delete_cwt_view(request,pk):
    cwt=models.CourseWiseTeacher.objects.get(id=pk)
    cwt.delete()
    return HttpResponseRedirect('/admin-view-cwt')

@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'exam/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=models.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'exam/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'exam/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'exam/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'exam/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'exam/admin_check_marks.html',{'results':results})
    




def aboutus_view(request):
    return render(request,'exam/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form':sub})


def mail_test(request):

    # EmailMessage('Subject', 'Body', to=['abdurroufcse46@gmail.com']).send()
    #ssssend_mail('test email', 'hello world', to=['abdurroufcse46@gmail.com'])
    send_mail('Online examination system', 'Hello , This a test mail from online-examination-system created by Mr.Mushfiq', 'onlineexamination2k20@gmail.com', ['hasanhasibul395@gmail.com'],
             fail_silently=False)



def forget_pass(request):
    pass

@login_required(login_url='studentlogin')
def test_exam(request,pk):
    if request.method == 'POST':
        data = request.POST
        datadict = dict(data)
        student = models.Student.objects.get(user_id=request.user.id)
        course = QMODEL.Course.objects.get(id=pk)
        examattend = QMODEL.Examattend()
        examattend.student = student
        examattend.course = course
        examattend.save()

        for k in datadict:
            if 'csrfmiddlewaretoken' not in k:
                value = datadict.get(k)[0]
                keymain = k
                key = k.split('_')
                datalist = list(key)
                questiontype = datalist[1]
                if questiontype != '2':
                    questionid = datalist[0]
                    course_id = datalist[2]
                    answer = value
                    status = 1
                    student1 = models.Student.objects.get(user_id=request.user.id)
                    course1 = QMODEL.Course.objects.get(id=course_id)
                    examans = QMODEL.QuestionAns()
                    examans.answer = answer
                    examans.status = status
                    examans.course = QMODEL.Course.objects.get(id=course_id)
                    examans.question = QMODEL.Question.objects.get(id=questionid)
                    examans.questiontype = questiontype
                    examans.student = models.Student.objects.get(user_id=request.user.id)
                    examans.save()

        if request.FILES:
            data2 = request.FILES
            datadict2 = dict(data2)

            for d in datadict2:
                data_key = d.split('_')
                datakeylist = list(data_key)
                fileqtype = datakeylist[1]
                questionid = datakeylist[0]
                course_id = datakeylist[2]
                status = 1
                examans = QMODEL.QuestionAns()
                examans.status = status
                examans.course = QMODEL.Course.objects.get(id=course_id)
                examans.question = QMODEL.Question.objects.get(id=questionid)
                examans.questiontype = fileqtype
                examans.student = models.Student.objects.get(user_id=request.user.id)
                examans.uploadedFile = request.FILES[d]
                examans.save()


        return HttpResponseRedirect('/student/view-result')


    else:
        course = QMODEL.Course.objects.get(id=pk)
        questions = QMODEL.Question.objects.all().filter(course=course)
        student = models.Student.objects.get(user_id=request.user.id)
        attendexam = QMODEL.Examattend.objects.all().filter(student=student,course=course).first()
        import pdb; pdb.set_trace()

        response = render(request, 'exam/test.html', {'course': course, 'questions': questions, 'status':attendexam})
        response.set_cookie('course_id', course.id)

    return response


