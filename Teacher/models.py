from datetime import datetime
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class ClassTeachers(models.Model):   
    teach_id = models.IntegerField()
    class_code = models.CharField(max_length=10)
    class_name = models.CharField(max_length=40)
    class Meta:
        db_table = "ClassTeachers"
    def __str__(self):
         return self.class_name + " - "+self.class_code

class Assignments(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_name = models.CharField(max_length=40)
    assignment_description = models.CharField(max_length=100)
    class_code = models.CharField(max_length=10)
    max_marks = models.FloatField(default=25)
    peer_grade = models.BooleanField(default=False)
    class Meta:
        db_table = "Assignments"
    def __str__(self):
         return self.assignment_name +" - "+ self.class_code

class PeerGrade(models.Model):
    peergrade_id = models.AutoField(primary_key=True)
    stud_id = models.IntegerField()
    assign_id = models.IntegerField()
    peer_1 = models.IntegerField()
    peer_2 = models.IntegerField()
    class Meta:
        db_table = "PeerGrade"

class Announcements(models.Model):
    teach_id = models.IntegerField()
    class_code = models.CharField(max_length=10)
    announce_data = models.CharField(max_length=1000)
    date = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = "Announcements"
    def __str__(self):
         return self.announce_data +" - "+ self.class_code


class Schedule(models.Model):
    teach_id = models.IntegerField()
    class_code = models.CharField(max_length=10)
    event_data = models.CharField(max_length=1000)
    event_date = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = "Schedule"
    def __str__(self):
         return self.event_data +" - "+ self.class_code