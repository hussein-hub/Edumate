from django.db import models

# Create your models here.

class ClassStudents(models.Model):
    class_code = models.CharField(max_length=10)
    stud_id = models.IntegerField()
    class Meta:
        db_table = "ClassStudents"