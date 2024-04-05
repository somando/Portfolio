from django.contrib import admin
from .models import *

# Register your models here.

class StaticProfileDataAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name_en', 'name_ja', 'nickname', 'description')

admin.site.register(StaticProfileData, StaticProfileDataAdmin)


class ProfileDataAdmin(admin.ModelAdmin):
    list_display = ('fontawesome', 'detail', 'url')
    search_fields = ('detail',)

admin.site.register(ProfileData, ProfileDataAdmin)

class ExperienceDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'detail', 'show_top', 'link_title', 'link_url')
    list_filter = ('show_top', 'date',)
    search_fields = ('title', 'detail', 'link_title',)

admin.site.register(ExperienceData, ExperienceDataAdmin)

class ProductsDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'date', 'team', 'prize', 'github', 'image', 'show_top', 'link_title', 'link_url')
    list_filter = ('show_top', 'date',)
    search_fields = ('title', 'event', 'team', 'prize', 'link_title',)

admin.site.register(ProductsData, ProductsDataAdmin)

class SkillDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_id', 'detail')
    search_fields = ('title', 'icon_id', 'detail',) 

admin.site.register(SkillData, SkillDataAdmin)
