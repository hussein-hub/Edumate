from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from Teacher.views import assignmentgrade
from . import views

urlpatterns = [
    path('', views.stud_home, name='student_home'),
    path('classroom/<pk2>/', views.classroom, name='classroom1'),
    path('classroom/<pk2>/announcement/', views.announcement_stud, name='announcement_stud'),
    path('classroom/<pk2>/schedule/', views.schedule.as_view(), name='schedule_student'),
    path('classroom/<pk2>/assignment/<pk3>/', views.assignmentsub, name='assignment'),
    path('classroom/<pk2>/quiz/', views.quiz, name='quiz_stud'),
    path('classroom/<pk2>/quiz/<pk3>', views.ansquiz, name='ansquiz'),
    path('classroom/<pk2>/quiz/review/<pk3>', views.revquiz, name='review_quiz'),
    path('classroom/<pk2>/submitatt/', views.enterattcode, name='submitatt'),
    path('classroom/<pk2>/submitatt/<pk3>/', views.submitatt, name='markatt'),
    path('classroom/<pk2>/porjecttrack/', views.projecttrack, name='sporjecttrack'),
    path('classroom/<pk2>/projecttrack/<pk3>/', views.single_project, name='single_project'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
