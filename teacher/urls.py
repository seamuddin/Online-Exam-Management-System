from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('teacherclick', views.teacherclick_view),
path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teachersignup', views.teacher_signup_view,name='teachersignup'),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-add-exam/<int:pk>', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),
path('delete-cws/', views.delete_cws_view,name='delete-cws'),
path('teacher-add-cws/<int:pk>', views.admin_add_cws_view,name='teacher-add-cws'),


path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher-question-marking', views.teacher_view_question_mark_view,name='teacher-question-marking'),
path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('see-answer/<int:pk>', views.see_answer_view,name='see-answer'),
path('view_answer_mark', views.view_answer_mark_view,name='view_answer_mark'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),
]