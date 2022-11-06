from django.urls import path

from . import views
urlpatterns = [
    path('', views.stud_home, name='student_home'),
    path('classroom/<pk2>/', views.classroom, name='classroom1'),
    path('classroom/<pk2>/assignment/<pk3>/', views.assignmentsub, name='assignment')
]