# Generated by Django 5.0.3 on 2024-05-03 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('somando', '0009_contactmessagedata_contactroomdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactroomdata',
            name='progress',
        ),
    ]
