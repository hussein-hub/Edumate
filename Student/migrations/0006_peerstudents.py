# Generated by Django 4.1 on 2022-11-17 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0005_alter_classstudents_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeerStudents',
            fields=[
                ('peerstud_id', models.AutoField(primary_key=True, serialize=False)),
                ('stud_id', models.IntegerField()),
                ('assign_id', models.IntegerField()),
                ('as_peer_1', models.IntegerField()),
                ('as_1_marks', models.FloatField()),
                ('as_peer_2', models.IntegerField()),
                ('as_2_marks', models.FloatField()),
            ],
            options={
                'db_table': 'PeerStudents',
            },
        ),
    ]
