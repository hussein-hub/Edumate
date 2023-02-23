from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(SubmittedAssignments)
admin.site.register(PeerStudents)
admin.site.register(Quiz_marks)

admin.site.register(ClassStudents)
# class ClassStudentsAdmin(admin.ModelAdmin):
	# list_display = ("class_code", "announce_data", "date")