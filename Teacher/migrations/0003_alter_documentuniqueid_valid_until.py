# Generated by Django 4.1 on 2023-03-25 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0002_alter_documentuniqueid_valid_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentuniqueid',
            name='valid_until',
            field=models.CharField(default='1679748634.6683555', max_length=200),
        ),
    ]