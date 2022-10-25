from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name="register"),
    path('final_registration/', views.final_reg, name="final_register"),
    path('login_student/', views.login_student, name='login_student'),
    path('login_teacher/', views.login_teacher, name='login_teacher'),
    path('student/<int:pk>/', include('Student.urls')),
    path('teacher/<int:pk>/', include('Teacher.urls')),
]