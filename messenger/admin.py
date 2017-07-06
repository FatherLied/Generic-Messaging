from django.contrib import admin
from .models import MessageThread, Message, Profile, ProfileThread, MessageManager

# Register your models here.
admin.site.register(MessageThread)
admin.site.register(Message)
admin.site.register(Profile)
# admin.site.register(MessageManager)
admin.site.register(ProfileThread)