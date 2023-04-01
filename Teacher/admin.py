from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ClassTeachers)
# admin.site.register(Assignments)

@admin.register(Assignments)
class AssignmentsAdmin(admin.ModelAdmin):
    list_display = ("assignment_id", "assignment_name", "class_code", "max_marks", "peer_grade", "duedate")


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
	list_display = ("teach_id", "class_code", "event_data", "event_date")


class OptionsInline(admin.TabularInline):
    model = Options


class ImageInline(admin.TabularInline):
    model = QuestionImage

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionsInline, ImageInline]

class att_img_inline(admin.TabularInline):
    model = Attendance_images
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("teacher_id", "class_id", "att_id", "start_time", "end_time", "code")
    inlines = [att_img_inline]

admin.site.register(QuestionImage)

admin.site.register(Question,QuestionAdmin)
admin.site.register(Options)
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(Attendance_images)
# admin.site.register(AttStud)

@admin.register(AttStud)
class AttStudAdmin(admin.ModelAdmin):
     list_display = ("att_id" , "stud_id", "att_time", "img_number")

# admin.site.register(Project)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
     list_display = ("pro_id", "class_code", "proj_name", "proj_due", "num_studs")

# admin.site.register(Groups)

@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
     list_display = ("group_id", "pro_id")

# admin.site.register(Members)

@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):
        list_display = ("mem_id", "group_id", "stud_id")

# admin.site.register(PeerGrade)
# admin.site.register(Quiz)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("quiz_name", "time_limit", "quiz_date", "teach_id", "class_code")

admin.site.register(Peergrade)
admin.site.register(PeerAssigns)

