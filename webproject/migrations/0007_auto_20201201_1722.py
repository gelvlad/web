# Generated by Django 3.1.2 on 2020-12-01 17:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webproject', '0006_auto_20201201_1711'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestAnswers',
            new_name='TestResults',
        ),
    ]
