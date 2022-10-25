from django.urls import path

from . import views
urlpatterns = [
    path('', views.teach_home, name='teacher_home'),
]