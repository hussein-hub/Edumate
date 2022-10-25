from django.urls import path

from . import views
urlpatterns = [
    path('', views.stud_home, name='student_home'),
]