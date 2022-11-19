from django.urls import path
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('', views.teach_home, name='teacher_home'),
    path('classroom/<pk2>/', views.classroom, name="classroom"),
    path('classroom/<pk2>/assignment/<pk3>/', views.assignmentsub, name='assignmentteach'),
    path('classroom/<pk2>/announcement', views.announcement, name='announcementteach'),
    path('classroom/<pk2>/announcement/<int:id>/', views.delete, name='delete'),
    path('classroom/<pk2>/assignment/<pk3>/grade/<pk4>', views.assignmentgrade, name='grade')
]
    
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)