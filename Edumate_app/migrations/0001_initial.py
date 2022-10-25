# Generated by Django 4.1 on 2022-10-25 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('stud_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('teach_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Teachers',
            },
        ),
    ]
