# Generated by Django 5.0.1 on 2025-04-10 07:41

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0007_studentsubmission'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentsubmission',
            unique_together={('student', 'assignment')},
        ),
    ]
