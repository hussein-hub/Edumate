from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ClassTeachers)
admin.site.register(Assignments)
admin.site.register(PeerGrade)

@admin.register(Announcements)
class AnnouncementsAdmin(admin.ModelAdmin):
	list_display = ("class_code", "announce_data", "date")

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
	list_display = ("class_code", "event_data", "event_date")