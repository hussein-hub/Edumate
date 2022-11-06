from django.db import models
import os

# Create your models here.

class ClassStudents(models.Model):
    class_code = models.CharField(max_length=10)
    stud_id = models.IntegerField()
    class Meta:
        db_table = "ClassStudents"

class SubmittedAssignments(models.Model):
    assign_id = models.AutoField(primary_key=True)
    assign_desc = models.CharField(max_length=100)
    assign_file = models.FileField(upload_to='Student/static/upload/')
    assignment_id = models.IntegerField()
    stud_id = models.IntegerField(default=0)
    class Meta:
        db_table = "SubAssigns"