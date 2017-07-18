from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Message, MessageThread, Archive
from django.views import View
import time


class AddMessageView(View): 
    
    def post(self, request):
        content = request.POST.get('content')
        thread_id = request.POST.get('thread_id')
        thread = MessageThread.objects.get(pk=thread_id)
        message = Message.objects.add_message(content=content, 
            thread=thread, sender=request.user)
        t = message.when_created.strftime("%B %d, %Y, %-I:%M %p")
        
        return JsonResponse({'content': message.content, 
            'when': t, 'sender': message.sender.username})

def download_csv(request, archive_obj):
    pass