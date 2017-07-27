from django.contrib import admin
from .models import MessageThread, Message, Profile, ProfileThread, Archive, SiteProfile

# Register your models here.
admin.site.register(MessageThread)
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(ProfileThread)
admin.site.register(Archive)
admin.site.register(SiteProfile)