from django.db import models
from teacher import models as TMODEL
from student.models import Student
import datetime

class Course(models.Model):
    exam_course = models.CharField(max_length=50, default=0)
    course_name = models.CharField(max_length=50)
    exam_type = models.CharField(max_length=50, default=0)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    start_time = models.CharField(max_length=100,default='0')
    end_time = models.CharField(max_length=100,default='0')
    created_by = models.CharField(max_length=40, default='0')
    def __str__(self):
        return self.course_name

class Department(models.Model):
    dept_name =  models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name

class QCourse(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    course_dept = models.ForeignKey(Department,on_delete=models.CASCADE)
    course_dept_name = models.CharField(max_length=100, default=0)

    def __str__(self):
        return self.course_name

class CourseWiseTeacher(models.Model):
    course = models.ForeignKey(QCourse, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TMODEL.Teacher, on_delete=models.CASCADE, null=True)

class CourseWiseStudent(models.Model):
    course = models.ForeignKey(QCourse, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)


class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    questiontype=models.CharField(max_length=200, default=0)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

class Examattend(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status =  models.CharField(max_length=100, default=0)



class QuestionAns(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    marks = models.CharField(max_length=200)
    questiontype = models.CharField(max_length=200, default=0)
    uploadedFile = models.FileField(blank=True,upload_to="Uploaded Files/", )
    dateTimeOfUpload = models.DateTimeField(auto_now=True)

