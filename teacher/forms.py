from django import forms
from django.contrib.auth.models import User
from . import models
from exam import models as QMODEL

class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class TeacherForm(forms.ModelForm):
    department =  forms.ModelChoiceField(queryset=QMODEL.Department.objects.all(), empty_label="Department Name",to_field_name="id")
    class Meta:
        model=models.Teacher
        fields=['email','mobile','profile_pic','teacher_id']

