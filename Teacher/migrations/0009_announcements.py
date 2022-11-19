# Generated by Django 4.1.3 on 2022-11-19 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0008_peergrade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teach_id', models.IntegerField()),
                ('class_code', models.CharField(max_length=10)),
                ('announce_data', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'Announcements',
            },
        ),
    ]
