# Generated by Django 5.0.3 on 2024-04-05 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('somando', '0006_productsdata_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productsdata',
            old_name='detail',
            new_name='about',
        ),
        migrations.RemoveField(
            model_name='skilldata',
            name='date',
        ),
    ]