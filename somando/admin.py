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
    list_display = ('date', 'title', 'detail', 'show_top', 'link')
    list_filter = ('show_top', 'date',)
    search_fields = ('title', 'detail', 'link')

admin.site.register(ExperienceData, ExperienceDataAdmin)

class ProductsDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'date', 'team', 'prize', 'github', 'image', 'show_top', 'link')
    list_filter = ('show_top', 'date',)
    search_fields = ('title', 'event', 'team', 'prize',)

admin.site.register(ProductsData, ProductsDataAdmin)

class SkillDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_id', 'detail')
    search_fields = ('title', 'icon_id', 'detail',) 

admin.site.register(SkillData, SkillDataAdmin)

class SkillCategoryDataAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'position')  
    search_fields = ('title_en', 'position')  

admin.site.register(SkillCategoryData, SkillCategoryDataAdmin)

class ContactRoomDataAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'auth_code', 'email', 'close')
    list_filter = ('close',)
    search_fields = ('room_id', 'email',)

admin.site.register(ContactRoomData, ContactRoomDataAdmin)

class ContactMessageDataAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'user', 'organization', 'admin', 'message', 'created_at')
    list_filter = ('admin', 'created_at',)
    search_fields = ('room_id', 'user', 'organization', 'message',)

admin.site.register(ContactMessageData, ContactMessageDataAdmin)
