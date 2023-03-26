from django.db import models
from django.utils import timezone

# Create your models here.

class ClassStudents(models.Model):
    class_code = models.ForeignKey("Teacher.ClassTeachers", on_delete=models.CASCADE, blank=True, null=True)
    stud_id = models.ForeignKey("Edumate_app.Students", on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        db_table = "ClassStudents"

class SubmittedAssignments(models.Model):
    assign_id = models.AutoField(primary_key=True)
    assign_desc = models.CharField(max_length=100)
    assign_file = models.FileField(upload_to='Student/static/upload/')
    assignment_id = models.ForeignKey("Teacher.Assignments", on_delete=models.CASCADE, blank=True, null=True)
    stud_id = models.ForeignKey("Edumate_app.Students", on_delete=models.CASCADE, blank=True, null=True)
    marks = models.FloatField(default=None, null=True)
    sub_date = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "SubAssigns"
    def get_student_name(self):
        return self.stud_id.name
    def __str__(self):
        return self.stud_id.name

class PeerStudents(models.Model):
    peerstud_id = models.AutoField(primary_key=True)
    stud_id = models.ForeignKey("Edumate_app.Students", on_delete=models.CASCADE, blank=True, null=True)
    assign_id = models.ForeignKey("Teacher.Assignments", on_delete=models.CASCADE, blank=True, null=True)
    as_peer_1 = models.ForeignKey("Edumate_app.Students", on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    as_1_marks = models.FloatField()
    as_peer_2 = models.ForeignKey("Edumate_app.Students", on_delete=models.CASCADE, blank=True, null=True, related_name="+")
    as_2_marks = models.FloatField()
    class Meta:
        db_table = "PeerStudents"

class Quiz_marks(models.Model):
    quiz = models.ForeignKey('Teacher.Quiz', on_delete=models.CASCADE, default=0, blank=True, null=True)
    student = models.ForeignKey('Edumate_app.Students', on_delete=models.CASCADE, default=0, blank=True, null=True)
    class_id = models.ForeignKey('Teacher.ClassTeachers', on_delete=models.CASCADE, blank=True, null=True)
    student_responses = models.TextField(null=True)
    correct_responses = models.TextField(null=True)
    total_marks = models.PositiveSmallIntegerField(default=0)
    marks_breakup = models.TextField(null=True)
    remarks = models.TextField(default="None", null=True)
    def __str__(self):
         return self.quiz.quiz_name +" - "+ self.student.name +" - "+ str(self.total_marks)