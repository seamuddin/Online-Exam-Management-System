from smtplib import SMTPException

from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse, BadHeaderError
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from student import models as SMODEL
from exam import forms as QFORM
import random


#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            if request.POST.get('email'):
                email = request.POST.get('email')
                randvalue = str(random.randint(20004, 200000000007))
                randstr1 = 'Hello, Here is your verification code ' + randvalue
                try:

                    send_mail('Online examination system',
                              randstr1,
                              'onlineexamination2k20@gmail.com', [email])
                    confirmemail = email


                except ValueError:

                    context1 = {
                        'error': 'Please Fill with the valid mail'
                    }
                    mydict.update(context1)
                    return render(request, 'teacher/teachersignup.html', context=mydict)
                if confirmemail:
                    teacher.verification = randvalue
                    teacher.save()
                    my_teacher_group = Group.objects.get_or_create(name='TEACHER')
                    my_teacher_group[0].user_set.add(user)




        return HttpResponseRedirect('teacherlogin')
    return render(request,'teacher/teachersignup.html',context=mydict)



def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.QCourse.objects.all().count(),
    'total_exam':QMODEL.Course.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    user_id = request.user.id
    teacher = models.Teacher.objects.get(user_id=user_id)
    cwt = QMODEL.CourseWiseTeacher.objects.all().filter(teacher = teacher.id)
    return render(request,'teacher/teacher_exam.html',{'context' : cwt})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request, pk):
    from datetime import datetime
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():
            exam = courseForm.save(commit=False)
            exam.exam_type = request.POST.get('exam_type')
            exam.exam_course = pk
            start_time = request.POST.get('start_time')
            start_time = start_time.replace('T', ' ')
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            exam.start_time = start_time
            end_time = request.POST.get('end_time')
            end_time = end_time.replace('T', ' ')
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
            exam.end_time = end_time
            exam.created_by = request.user.id
            exam.save()
        else:
            print("form is invalid")
        courses = QMODEL.Course.objects.all().filter(exam_course = pk)
        return render(request, 'teacher/teacher_view_exam.html', {'courses': courses})
    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm})

@login_required(login_url='teacherlogin')
def admin_add_cws_view(request, pk):
    CWSForm=QFORM.CWSForm()
    if request.method=='POST':
        CWSForm=QFORM.CWSForm(request.POST)
        if CWSForm.is_valid():
            CWS = CWSForm.save(commit=False)
            course = QMODEL.QCourse.objects.get(id=pk)
            student = SMODEL.Student.objects.get(id=request.POST.get('student_id'))
            CWS.course = course
            CWS.student = student
            CWS.save()
        else:
            print("form is invalid")
        courses = QMODEL.CourseWiseStudent.objects.all().filter(course=pk)
        return render(request, 'teacher/teacher_view_cws.html', {'courses': courses})
    return render(request,'teacher/teacher_add_cws.html',{'courseForm':CWSForm})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_cws_view(request):
    pk = request.GET.get('cws_name')
    course_id = request.GET.get('course')
    course=QMODEL.CourseWiseStudent.objects.filter(id=int(pk))
    course.delete()
    course = QMODEL.CourseWiseStudent.objects.all().filter(course_id=int(course_id))
    return render(request, 'teacher/teacher_view_cws.html',{'courses':course})

@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_mark_view(request):
    courses= QMODEL.Course.objects.all().filter(created_by=request.user.id)
    return render(request,'teacher/teacher_view_answer_mark.html',{'courses':courses})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)

        if questionForm.is_valid():

            question=questionForm.save(commit=False)
            course=QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            teacher = models.Teacher.objects.get(user_id=request.user.id)
            question.created_by = teacher.id
            questiontype = request.POST.get('questiont')
            question.questiontype=questiontype
            question.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request,'teacher/teacher_add_question.html',{'questionForm':questionForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    courses= QMODEL.Course.objects.all().filter(created_by=request.user.id)
    return render(request,'teacher/teacher_view_question.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_answer_view(request,pk):
    attend_info=QMODEL.Examattend.objects.all().filter(course_id=pk)
    print(attend_info)
    return render(request,'teacher/see_answer.html',{'context':attend_info})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def view_answer_mark_view(request):
    if request.POST:
        data_dict = dict(request.POST)
        new_list = []
        k =0
        for i in data_dict.keys():
            new_list.append(i)
        for j in data_dict:
            print(j)
            qans_info1 = QMODEL.QuestionAns.objects.get(id=j)
            mark = data_dict.get(j)[0]
            if mark == '':
                mark = 0
            k = k+int(mark)
            qans_info1.marks = int(mark)
            qans_info1.status = 0
            qans_info1.save()

        student = request.GET.get('student')
        course = request.GET.get('course')
        model1 = QMODEL.Result()
        model1.marks = k
        smodel = SMODEL.Student.objects.get(id=student)
        cmodel = QMODEL.Course.objects.get(id=course)
        model1.student = smodel
        model1.exam = cmodel
        model1.save()

    course = request.GET.get('course')
    cmodel = QMODEL.Course.objects.get(id=course)
    id = request.GET.get('student')
    qans_info=QMODEL.QuestionAns.objects.all().filter(student_id=int(id), course_id=cmodel.id)
    return render(request,'teacher/see_Q_ans.html',{'context':qans_info})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')
