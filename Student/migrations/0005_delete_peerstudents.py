# Generated by Django 4.1 on 2023-03-31 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0004_progress'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PeerStudents',
        ),
    ]