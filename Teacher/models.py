from datetime import datetime, timedelta
import time
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
from django.utils import timezone


class ClassTeachers(models.Model):   
    teach_id = models.ForeignKey("Edumate_app.Teachers", on_delete=models.CASCADE, blank=True, null=True)
    class_code = models.CharField(primary_key=True, max_length=10)
    class_name = models.CharField(max_length=40)
    class Meta:
        db_table = "ClassTeachers"
    def __str__(self):
         return self.class_name + " - "+self.class_code

class Assignments(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_name = models.CharField(max_length=40)
    assignment_description = models.CharField(max_length=100)
    class_code = models.ForeignKey(ClassTeachers, on_delete=models.CASCADE, blank=True, null=True)
    max_marks = models.FloatField(default=25)
    peer_grade = models.BooleanField(default=False)
    duedate =  models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "Assignments"
    def __str__(self):
         return self.assignment_name +" - "+ self.class_code.class_code
    
class Announcements(models.Model):
    ann_id = models.AutoField(primary_key=True)
    teach_id = models.ForeignKey("Edumate_app.Teachers", on_delete=models.CASCADE, blank=True, null=True)
    class_code = models.ForeignKey(ClassTeachers, on_delete=models.CASCADE, blank=True, null=True)
    announce_data = models.CharField(max_length=1000)
    date = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = "Announcements"
    def __str__(self):
         return self.announce_data +" - "+ self.class_code.class_code

class Schedule(models.Model):
    teach_id = models.ForeignKey("Edumate_app.Teachers", on_delete=models.CASCADE, blank=True, null=True)
    class_code = models.ForeignKey(ClassTeachers, on_delete=models.CASCADE, blank=True, null=True)
    event_data = models.CharField(max_length=1000)
    event_date = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = "Schedule"
    def __str__(self):
         return self.event_data +" - "+ self.class_code.class_code
         
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.teach_id.teach_id,self.class_code.class_code,self.id,))
        return f'<a href="{url}"> {self.event_data} </a>'

class Quiz(models.Model):
    quiz_name = models.CharField(max_length=200)
    description= models.CharField(max_length=100, null=True)
    time_limit = models.PositiveBigIntegerField(default=10)
    quiz_date = models.DateTimeField(default=datetime.now)
    teach_id = models.ForeignKey("Edumate_app.Teachers", on_delete=models.CASCADE, blank=True, null=True)
    class_code = models.ForeignKey(ClassTeachers, on_delete=models.CASCADE, blank=True, null=True)    
    def __str__(self):
        return str(self.quiz_name)

class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, default=0, blank=True, null=True)
    question_name = models.CharField(max_length=1000)
    marks= models.PositiveIntegerField(null=True,default=0)
    def __str__(self):
        return str(self.question_name)

class Options(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=0, blank=True, null=True)
    option_name = models.CharField(max_length=1000)
    correct = models.BooleanField(default=False)
    def __str__(self):
        return str(self.option_name)

class QuestionImage(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=0, blank=True, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return str(self.question.question_name)

class Attendance(models.Model):
    teacher_id = models.ForeignKey("Edumate_app.Teachers", on_delete=models.CASCADE, blank=True, null=True)
    class_id = models.ForeignKey(ClassTeachers, on_delete=models.CASCADE, blank=True, null=True)
    att_id = models.AutoField(primary_key=True)
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    class Meta:
        db_table = "Attendance"
    def __str__(self):
         return self.code

class AttStud(models.Model):
    att_id = models.ForeignKey(Attendance, on_delete=models.CASCADE, blank=True, null=True)
    stud_id = models.ForeignKey("Edumate_app.Students", on_delete=models.CASCADE, blank=True, null=True)
    att_time = models.CharField(max_length=100)
    img_number = models.IntegerField(default=0)
    class Meta:
        db_table = "AttStud"

class Plagarism(models.Model):
    assignment_id = models.ForeignKey(Assignments, on_delete=models.CASCADE, default=0, blank=True, null=True)
    stud_assignment1 = models.ForeignKey('Student.SubmittedAssignments', on_delete=models.CASCADE, default=0, related_name="assignment1", blank=True, null=True)
    stud_assignment2 = models.ForeignKey('Student.SubmittedAssignments', on_delete=models.CASCADE, default=0, related_name="assignment2", blank=True, null=True)
    percentage_similarity = models.FloatField(default=0)
    class Meta:
        db_table = "similarity"
    def __str__(self):
        return str(self.assignment_id)

class Attendance_images(models.Model):
    att_id = models.ForeignKey(Attendance, on_delete=models.CASCADE, blank=True, null=True)
    att_image = models.ImageField(upload_to='images/', null=True, blank=True)
    class Meta:
        db_table = "attendance_images"
    # def __str__(self):
    #     return str(self.att_image)

class DocumentUniqueID(models.Model):
    doc_id = models.AutoField(primary_key=True)
    plagarism_id = models.ForeignKey(Plagarism, on_delete=models.CASCADE, blank=True, null=True)
    doc_unique_id = models.CharField(max_length=100)
    valid_until = models.CharField(default=str(time.time()), max_length=200)
    url = models.CharField(default="", max_length=1000)
    class Meta:
        db_table = "DocumentUniqueID"

class Project(models.Model):
    pro_id = models.AutoField(primary_key=True)
    class_code = models.ForeignKey(ClassTeachers, on_delete=models.CASCADE, blank=True, null=True)
    proj_name = models.CharField(max_length=100)
    proj_desc = models.CharField(max_length=300)
    proj_due = models.DateTimeField(default=datetime.now)
    prog_check = models.CharField(max_length=500)
    num_studs = models.IntegerField(default=2)
    class Meta:
        db_table = "Project"
    def __str__(self):
        return str(self.proj_name)

class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    pro_id = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        db_table = "Groups"
    def __str__(self):
        return str(self.group_id)

class Members(models.Model):
    mem_id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, blank=True, null=True)
    stud_id = models.ForeignKey("Edumate_app.Students", on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        db_table = "Members"
    def __str__(self):
        return str(self.mem_id)

class Peergrade(models.Model):
    peergrade_id = models.AutoField(primary_key=True)
    class_code = models.ForeignKey(ClassTeachers, on_delete=models.CASCADE, blank=True, null=True)
    assignment_id = models.ForeignKey(Assignments, on_delete=models.CASCADE, blank=True, null=True)
    number_of_peers = models.IntegerField(default=0)
    questions = models.CharField(max_length=1000, default=None, blank=True, null=True)
    opt1 = models.CharField(max_length=1000, default=None, blank=True, null=True)
    opt2 = models.CharField(max_length=1000, default=None, blank=True, null=True)
    opt3 = models.CharField(max_length=1000, default=None, blank=True, null=True)
    class Meta:
        db_table = "Peergrade"

class PeerAssigns(models.Model):
    peergrade_id = models.ForeignKey(Peergrade, on_delete=models.CASCADE, blank=True, null=True)
    stud_id = models.ForeignKey("Edumate_app.Students", on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    assigned_stud_id = models.ForeignKey("Edumate_app.Students", on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    feedb = models.CharField(max_length=100, default=None, blank=True, null=True)
    marks = models.FloatField(default=None, blank=True, null=True)
    options_selec = models.CharField(max_length=1000, default=None, blank=True, null=True)
    class Meta:
        db_table = "Peerassigns"


