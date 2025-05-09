# Generated by Django 5.0.1 on 2025-04-16 18:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0012_quiz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=512)),
                ('option_a', models.CharField(max_length=256)),
                ('option_b', models.CharField(max_length=256)),
                ('option_c', models.CharField(max_length=256)),
                ('option_d', models.CharField(max_length=256)),
                ('correct_option', models.CharField(max_length=1)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='courses_app.quiz')),
            ],
        ),
    ]
