from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    email = models.CharField(max_length=40, default=0)
    teacher_id = models.CharField(max_length=30, default=0)
    department = models.CharField(max_length=40, default=0)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    verification = models.CharField(max_length=20, default=0)
    verify_state = models.IntegerField(default=0)
    salary=models.PositiveIntegerField(null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name


