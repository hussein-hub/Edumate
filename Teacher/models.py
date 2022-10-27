from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class ClassTeachers(models.Model):   
    teach_id = models.IntegerField()
    class_code = models.CharField(max_length=10)
    class_name = models.CharField(max_length=40)
    class Meta:
        db_table = "ClassTeachers"