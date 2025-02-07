# Generated by Django 5.0.2 on 2025-02-07 05:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('somando', '0018_remove_experiencedata_link_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillCategoryData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('position', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='skilldata',
            name='position',
            field=models.IntegerField(default=None, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skilldata',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='somando.skillcategorydata'),
        ),
    ]
