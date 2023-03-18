from django.db import models
import os
from Teacher.models import *
from Edumate_app.models import *

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
    marks = models.FloatField(default=None, null=True)
    sub_date = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "SubAssigns"
    def get_student_name(self):
        return Students.objects.get(stud_id=self.stud_id).name
    def __str__(self):
         myid = self.stud_id
         a = Students.objects.get(stud_id = myid).name
         return str(a)

class PeerStudents(models.Model):
    peerstud_id = models.AutoField(primary_key=True)
    stud_id = models.IntegerField()
    assign_id = models.IntegerField()
    as_peer_1 = models.IntegerField()
    as_1_marks = models.FloatField()
    as_peer_2 = models.IntegerField()
    as_2_marks = models.FloatField()
    class Meta:
        db_table = "PeerStudents"


class Quiz_marks(models.Model):
    quiz = models.ForeignKey('Teacher.Quiz', on_delete=models.CASCADE, default=0)
    student = models.ForeignKey('Edumate_app.Students', on_delete=models.CASCADE, default=0)
    class_id = models.CharField(max_length=10)
    student_responses = models.TextField(null=True)
    correct_responses = models.TextField(null=True)
    total_marks = models.PositiveSmallIntegerField(default=0)
    marks_breakup = models.TextField(null=True)

    def __str__(self):
         return self.quiz.quiz_name +" - "+ self.student.name +" - "+ str(self.total_marks)