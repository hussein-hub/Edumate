# Generated by Django 4.1 on 2023-03-31 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0011_peerassigns_feedb_peerassigns_marks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='peergrade',
            name='number_of_peers',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='documentuniqueid',
            name='valid_until',
            field=models.CharField(default='1680274626.250561', max_length=200),
        ),
    ]
