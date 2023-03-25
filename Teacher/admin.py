from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ClassTeachers)
admin.site.register(Assignments)
admin.site.register(PeerGrade)
admin.site.register(Quiz)

@admin.register(DocumentUniqueID)
class DocumentUniqueIDAdmin(admin.ModelAdmin):
    list_display = ("doc_id", "plagarism_id", "doc_unique_id")

@admin.register(Plagarism)
class PlagarismAdmin(admin.ModelAdmin):
	list_display = ("id", "assignment_id", "stud_assignment1", "stud_assignment2", "percentage_similarity")



@admin.register(Announcements)
class AnnouncementsAdmin(admin.ModelAdmin):
	list_display = ("class_code", "announce_data", "date")

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
	list_display = ("class_code", "event_data", "event_date")


class OptionsInline(admin.TabularInline):
    model = Options


class ImageInline(admin.TabularInline):
    model = QuestionImage

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionsInline, ImageInline]

class att_img_inline(admin.TabularInline):
    model = Attendance_images
class AttendanceAdmin(admin.ModelAdmin):
    inlines = [att_img_inline]

admin.site.register(QuestionImage)

admin.site.register(Question,QuestionAdmin)
admin.site.register(Options)
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(Attendance_images)
admin.site.register(AttStud)
admin.site.register(Project)
admin.site.register(Groups)
admin.site.register(Members)