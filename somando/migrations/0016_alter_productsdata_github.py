# Generated by Django 4.2.11 on 2024-07-25 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('somando', '0015_experiencedata_draft_productsdata_draft_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsdata',
            name='github',
            field=models.TextField(blank=True),
        ),
    ]