# Generated by Django 4.1 on 2023-03-31 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0006_alter_documentuniqueid_valid_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentuniqueid',
            name='valid_until',
            field=models.CharField(default='1680270984.6264317', max_length=200),
        ),
    ]