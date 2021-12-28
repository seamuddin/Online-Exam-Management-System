from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        fields=['course_name','question_number','total_marks']

class QCourseForm(forms.ModelForm):
    dept_id = forms.ModelChoiceField(queryset=models.Department.objects.all(), empty_label="Department Name",to_field_name="id")
    class Meta:
        model=models.QCourse
        fields=['course_name','course_code']

class DeptForm(forms.ModelForm):
    class Meta:
        model=models.Department
        fields=['dept_name']

class DeptForm(forms.ModelForm):
    class Meta:
        model=models.Department
        fields=['dept_name']

class CWTForm(forms.ModelForm):
    course_id = forms.ModelChoiceField(queryset=models.QCourse.objects.all(), empty_label="Course Name", to_field_name="id")
    teacher_id = forms.ModelChoiceField(queryset=models.TMODEL.Teacher.objects.all(), empty_label="Teacher Name", to_field_name="id")
    class Meta:
        model=models.CourseWiseTeacher
        fields=['course_id']


DEMO_CHOICES =(
    ("0", "MCQ"),
    ("1", "Written"),
    ("2", "Attachment"),
)



class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = False

    #this will show dropdown __str__ method course model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in course model and return it
    questiont = forms.ChoiceField(choices=DEMO_CHOICES)
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Question
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
        required = (
            'option1',
            'option2',
            'option3',
            'option4',
            'answer',
        )
