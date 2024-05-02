from django.db import models

# Create your models here.
class StaticProfileData(models.Model):
    icon = models.URLField()
    name_en = models.CharField(max_length=100)
    name_ja = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    description = models.TextField()

class ProfileData(models.Model):
    fontawesome = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)
    url = models.CharField(max_length=100, blank=True)

class ExperienceData(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    detail = models.TextField(blank=True)
    show_top = models.BooleanField(default=False)
    link_title = models.CharField(max_length=100, blank=True)
    link_url = models.URLField(blank=True)

class ProductsData(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, blank=True)
    event = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    team = models.CharField(max_length=100, blank=True)
    prize = models.CharField(max_length=100, blank=True)
    github = models.URLField(blank=True)
    image = models.URLField(blank=True)
    about = models.TextField(blank=True)
    detail = models.TextField(blank=True)
    technology = models.TextField(blank=True)
    infrastracture = models.TextField(blank=True)
    show_top = models.BooleanField(default=False)
    link_title = models.CharField(max_length=100, blank=True)
    link_url = models.URLField(blank=True)

class SkillData(models.Model):
    title = models.CharField(max_length=100)
    icon_id = models.CharField(max_length=100)
    detail = models.TextField(blank=True)

class ContactRoomData(models.Model):
    room_id = models.CharField(max_length=20, unique=True)
    auth_code = models.CharField(max_length=6, blank=True)
    email = models.EmailField()
    progress = models.BooleanField(default=False)
    close = models.BooleanField(default=False)

class ContactMessageData(models.Model):
    room_id = models.CharField(max_length=20)
    user = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, blank=True)
    admin = models.BooleanField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
