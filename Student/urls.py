from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from Teacher.views import assignmentgrade
from . import views
urlpatterns = [
    path('', views.stud_home, name='student_home'),
    path('classroom/<pk2>/', views.classroom, name='classroom1'),
    path('classroom/<pk2>/announcement', views.announcement_stud, name='announcement_stud'),
    path('classroom/<pk2>/assignment/<pk3>/', views.assignmentsub, name='assignment'),
    
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)