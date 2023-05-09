from django.urls import path
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('', views.teach_home, name='teacher_home'),
    path('classroom/<pk2>/', views.classroom, name="classroom"),
    path('deleteclass/', views.deleteclass, name="deleteclass"),
    path('classroom/<pk2>/teacher_analytics/', views.teacher_analytics, name='teacher_analytics'),
    path('classroom/<pk2>/students/', views.all_students, name='all_students'),
    path('classroom/<pk2>/assignment/<pk3>/', views.assignmentsub, name='assignmentteach'),
    path('classroom/<pk2>/assignment/<pk3>/grades/', views.viewgrades, name='viewgrades'),
    path('classroom/<pk2>/deleteassignment/', views.assignmentdelete, name='assignmentdelete'),
    path('classroom/<pk2>/assignment/<pk3>/similarity_check', views.assignmentSimilarityCheck, name='assignmentSimilarityCheck'),
    path('classroom/<pk2>/announcement', views.announcement, name='announcementteach'),
    path('classroom/<pk2>/deleteannouncement/', views.ann_delete, name='announcementdelete'),
    path('classroom/<pk2>/schedule/', views.schedule.as_view(), name='schedule'),
    path("classroom/<pk2>/event/new/", views.event, name="event_new"),
    path("classroom/<pk2>/event/edit/<int:id>", views.event, name="event_edit"),
    path('classroom/<pk2>/assignment/<pk3>/grade/<pk4>', views.assignmentgrade, name='grade'),
    path('classroom/<pk2>/create_quiz', views.create_quiz, name="create_quiz"),
    path('classroom/<pk2>/attendance', views.attendance, name="attendance"),
    path('classroom/<pk2>/attendance/deleteatt', views.deleteatt, name="deleteatt"),
    path('classroom/<pk2>/attendance/<int:pk3>/', views.view_att, name="viewatt"),
    path('classroom/<pk2>/create_quiz/quiz_info/<pk3>', views.quiz_info, name="quiz_info"),
    path('classroom/<pk2>/projecttracking/', views.projecttracking, name='projecttracking'),
    path('classroom/<pk2>/deleteproject/', views.deletepro, name='projectdelete'),
    path('classroom/<pk2>/fetchcheck/', views.fetchcheck, name='fetchcheck'),
    path('classroom/<pk2>/projecttracking/<pk3>/', views.view_groups, name='view_groups'),
    path('classroom/<pk2>/projecttracking/<pk3>/group_details/<pk4>/', views.group_details, name='group_details'),
    path('classroom/<pk2>/assignment/<pk3>/details/', views.details, name='details'),
    path('classroom/<pk2>/peergroups/', views.grouppeergrading, name='grouppeergrading'),
    path('classroom/<pk2>/peergroups/deletegroup/', views.delgroup, name='delgroup'),
    path('classroom/<pk2>/peergroups/<pk3>/', views.showpeergroups, name='showpeergroups'),
    path('classroom/<pk2>/peergroups/<pk3>/view_grades/', views.view_grades, name='view_grades'),
    path('classroom/<pk2>/peergroups/<pk3>/showassignment/<pk4>/', views.groupgrade, name='groupgrade'),
    # path('video_feed', views.video_feed, name='video_feed'),
    path('logout/', views.logout, name="logout")
]
    
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)