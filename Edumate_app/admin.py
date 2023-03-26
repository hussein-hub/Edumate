from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Students)
# admin.site.register(Teachers)


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ("stud_id", "name")

@admin.register(Teachers)
class TeachersAdmin(admin.ModelAdmin):
    list_display = ("teach_id", "name")