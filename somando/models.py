from django.db import models

# Create your models here.
class StaticProfileData(models.Model):
    display_image = models.URLField()
    icon = models.URLField()
    name_en = models.CharField(max_length=100)
    name_ja = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    description = models.TextField()

class ProfileData(models.Model):
    fontawesome = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)
    url = models.CharField(max_length=100, blank=True)
    draft = models.BooleanField(default=False)

class ExperienceData(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    detail = models.TextField(blank=True)
    show_top = models.BooleanField(default=False)
    link = models.TextField(blank=True)
    draft = models.BooleanField(default=False)

class ProductsData(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, blank=True)
    event = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    team = models.CharField(max_length=100, blank=True)
    prize = models.CharField(max_length=100, blank=True)
    github = models.TextField(blank=True)
    image = models.URLField(blank=True)
    about = models.TextField(blank=True)
    detail = models.TextField(blank=True)
    technology = models.TextField(blank=True)
    infrastracture = models.TextField(blank=True)
    collaborators = models.TextField(blank=True)
    show_top = models.BooleanField(default=False)
    link = models.TextField(blank=True)
    draft = models.BooleanField(default=False)

class SkillCategoryData(models.Model):
    title_en = models.CharField(max_length=100)
    title_ja = models.CharField(max_length=100, null=True, blank=True)
    position = models.IntegerField(default=0, null=False)

class SkillData(models.Model):
    title = models.CharField(max_length=100)
    icon_id = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    detail = models.TextField(blank=True)
    position = models.IntegerField(default=0, null=False)
    show_top = models.BooleanField(default=True)
    category = models.ForeignKey(SkillCategoryData, on_delete=models.CASCADE, null=True, related_name='skills', blank=True)

class ContactRoomData(models.Model):
    room_id = models.CharField(max_length=20, unique=True)
    auth_code = models.CharField(max_length=6, blank=True)
    email = models.EmailField()
    close = models.BooleanField()

class ContactMessageData(models.Model):
    room_id = models.CharField(max_length=20)
    user = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, blank=True)
    admin = models.BooleanField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
