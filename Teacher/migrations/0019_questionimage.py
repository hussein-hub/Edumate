# Generated by Django 4.1.3 on 2023-01-15 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0018_quiz_question_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('question', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Teacher.question')),
            ],
        ),
    ]
