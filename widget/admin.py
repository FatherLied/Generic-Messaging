from django.contrib import admin
from .models import MessageThread, Message

# Register your models here.
admin.site.register(MessageThread)
admin.site.register(Message)