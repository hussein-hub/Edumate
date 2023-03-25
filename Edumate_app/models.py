from django.db import models

# Create your models here.
class Students(models.Model):   
    stud_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    is_change = models.IntegerField(default=0)
    class Meta:
        db_table = "Students"
    # def __str__(self):
    #      return str(self.name)

class Teachers(models.Model):   
    teach_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    is_change = models.IntegerField(default=0)
    class Meta:
        db_table = "Teachers"
    def __str__(self):
         return self.name