# Generated by Django 4.1 on 2023-03-31 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0007_alter_documentuniqueid_valid_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentuniqueid',
            name='valid_until',
            field=models.CharField(default='1680271068.4212008', max_length=200),
        ),
        migrations.DeleteModel(
            name='PeerGrade',
        ),
    ]
