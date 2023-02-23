from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

admin.site.site_header = 'Edumate'                    
admin.site.index_title = 'Edumate Admin'                
admin.site.site_title = 'Edumate Admin'

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('Edumate_app.urls')),
    
]
# if settings.DEBUG:
# 	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)