# Generated by Django 5.0.1 on 2025-04-06 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0003_course_image_alter_course_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
