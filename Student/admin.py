from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(SubmittedAssignments)

@admin.register(SubmittedAssignments)
class SubmittedAssignmentsAdmin(admin.ModelAdmin):
	list_display = ("assign_id", "assign_file", "assignment_id", "stud_id", "marks", "sub_date")

# admin.site.register(PeerStudents)

@admin.register(PeerStudents)
class PeerStudentsAdmin(admin.ModelAdmin):
	list_display = ("peerstud_id", "stud_id", "assign_id", "as_peer_1", "as_1_marks", "as_peer_2", "as_2_marks")

# admin.site.register(Quiz_marks)

@admin.register(Quiz_marks)
class Quiz_marksAdmin(admin.ModelAdmin):
	list_display = ("quiz", "student", "class_id", "total_marks", "remarks")

# admin.site.register(ClassStudents)

@admin.register(ClassStudents)
class ClassStudentsAdmin(admin.ModelAdmin):
	list_display = ("class_code", "stud_id")

admin.site.register(Progress)