# Generated by Django 5.0.3 on 2024-04-02 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('somando', '0003_alter_experiencedata_link_url_alter_profiledata_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsdata',
            name='detail',
            field=models.TextField(blank=True),
        ),
    ]
