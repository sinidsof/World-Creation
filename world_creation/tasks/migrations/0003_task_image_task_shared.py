# Generated by Django 5.1.3 on 2024-12-08 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_selfassessment'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='task_images/'),
        ),
        migrations.AddField(
            model_name='task',
            name='shared',
            field=models.BooleanField(default=False),
        ),
    ]
