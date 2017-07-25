
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View

from .models import Archive, Message, MessageThread

import time


class AddMessageView(View): 
    
    def post(self, request):
        content = request.POST.get('content')
        thread_id = request.POST.get('thread_id')
        thread = MessageThread.objects.get(pk=thread_id)
        message = Message.objects.add_message(content=content, 
            thread=thread, sender=request.user)
        t = message.when_created.strftime("%B %d, %Y, %-I:%M %p")
        return JsonResponse({'pk': message.pk,
            'threadId': message.thread_id, 
            'content': message.content, 
            'when': t, 
            'sender': message.sender.username, 
            'sender_pk': message.sender.pk
            })

def download_csv(request, archive_obj):
    pass


class RetrieveMessage(View):

    def get(self, request, *args, **kwargs):
        latest_id = request.GET['latestId']
        thread_id = request.GET['threadId']
        messages = Message.objects.filter(id__gt=latest_id, thread__id=thread_id)
        context = {}
        context['messages'] = []
        for message in messages:
            context['messages'].append({'pk': message.pk, 
                'content': message.content, 
                'when': message.when_created.strftime("%B %d, %Y, %-I:%M %p"), 
                'sender': message.sender.username, 
                'sender_pk': message.sender.pk})
        return JsonResponse({'objects': context})


