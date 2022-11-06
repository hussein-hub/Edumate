from django.urls import path

from . import views
urlpatterns = [
    path('', views.teach_home, name='teacher_home'),
    path('classroom/<pk2>/', views.classroom, name="classroom"),
    path('classroom/<pk2>/assignment/<pk3>/', views.assignmentsub, name='assignmentteach')
]