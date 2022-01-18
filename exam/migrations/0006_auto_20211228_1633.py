# Generated by Django 3.0.5 on 2021-12-28 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20211228_1633'),
        ('student', '0002_remove_student_status'),
        ('exam', '0005_auto_20201209_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='type',
        ),
        migrations.AddField(
            model_name='question',
            name='questiontype',
            field=models.CharField(default=0, max_length=200),
        ),
        migrations.CreateModel(
            name='QuestionAns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('marks', models.CharField(max_length=200)),
                ('questiontype', models.CharField(default=0, max_length=200)),
                ('uploadedFile', models.FileField(blank=True, upload_to='Uploaded Files/')),
                ('dateTimeOfUpload', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Course')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='QCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
                ('course_code', models.CharField(max_length=100)),
                ('course_dept_name', models.CharField(default=0, max_length=100)),
                ('course_dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Examattend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default=0, max_length=100)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='CourseWiseTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.QCourse')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher')),
            ],
        ),
    ]