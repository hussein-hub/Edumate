from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class ClassTeachers(models.Model):   
    teach_id = models.IntegerField()
    class_code = models.CharField(max_length=10)
    class_name = models.CharField(max_length=40)
    class Meta:
        db_table = "ClassTeachers"

class Assignments(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_name = models.CharField(max_length=40)
    assignment_description = models.CharField(max_length=100)
    class_code = models.CharField(max_length=10)
    max_marks = models.FloatField(default=25)
    class Meta:
        db_table = "Assignments"

class PeerGrade(models.Model):
    peergrade_id = models.AutoField(primary_key=True)
    stud_id = models.IntegerField()
    assign_id = models.IntegerField()
    peer_1 = models.IntegerField()
    peer_2 = models.IntegerField()
    class Meta:
        db_table = "PeerGrade"