# Generated by Django 3.2 on 2023-03-25 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentuniqueid',
            name='valid_until',
            field=models.CharField(default='1679744475.522241', max_length=200),
        ),
    ]