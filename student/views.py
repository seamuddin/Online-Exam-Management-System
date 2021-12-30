from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    course_id = request.GET.get('course')
    courses=QMODEL.Course.objects.all().filter(exam_course=int(course_id))
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):

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
        from datetime import datetime
        course = QMODEL.Course.objects.get(id=pk)
        questions = QMODEL.Question.objects.all().filter(course=course)
        student = models.Student.objects.get(user_id=request.user.id)
        attendexam = QMODEL.Examattend.objects.all().filter(student=student,course=course).first()
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        if course.start_time < dt_string < course.end_time:
            datetimeobj = datetime.strptime(course.end_time, "%Y-%m-%d %H:%M:%S")
            datetimeobj1 = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
            print(datetimeobj1)
            time = datetimeobj - datetimeobj1
            print(time)
            time = time.total_seconds()/60

            response = render(request, 'exam/test.html',
                              {'course': course, 'questions': questions, 'status': attendexam, 'time':time})
            response.set_cookie('course_id', course.id)
            return response

        else:
            return HttpResponseRedirect('/student/student-dashboard')










@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()


        return HttpResponseRedirect('view-result')



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_course_view(request):
    student = models.Student.objects.get(user_id=request.user.id)
    CWS = QMODEL.CourseWiseStudent.objects.all().filter(student=student.id)
    return render(request,'student/student_course_view.html',{'cws':CWS})