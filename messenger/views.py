
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View
from django.views import View

from .models import Message, MessageThread, Archive,Profile

import time


class AddMessageView(View): 
    
    def post(self, request):
        content = request.POST.get('content')
        thread_id = request.POST.get('thread_id')
        thread = MessageThread.objects.get(pk=thread_id)
        message = Message.objects.add_message(content=content, 
            thread=thread, sender=request.user)
        t = message.when_created.strftime("%B %d, %Y, %-I:%M %p")

        return JsonResponse({'pk': message.pk, 'content': message.content, 'when': t,
            'sender': message.sender.username, 'sender_pk': message.sender.pk})
        
class RetrieveMessage(View):

    def get(self, request, *args, **kwargs):
        latest_id = request.GET['latestId']
        thread_id = request.GET['threadId']
        messages = Message.objects.filter(id__gt=latest_id, thread__id=thread_id)
        context = {}
        context['messages'] = []
        for message in messages:
            context['messages'].append({'pk': message.pk, 'content': message.content, 
                'when': message.when_created.strftime("%B %d, %Y, %-I:%M %p"), 
                'sender': message.sender.username, 'sender_pk': message.sender.pk})
        return JsonResponse({'objects': context})

class ArchiveView(View):

    def post(self, request):
        requestor = request.POST['requestor']
        profile = Profile.objects.get(owner=request.user)
        print(profile)
        thread_id = request.POST['thread_id']
        print(requestor+":"+thread_id)
        thread = MessageThread.objects.get(pk=thread_id)
        archive = Archive.objects.create(thread=thread, requestor=profile)
        return HttpResponse('')
        # filename = archive.archive_file.name
        # response = HttpResponse(archive.archive_file, content_type='text/plain')
        # response['Content-Disposition'] = 'attachment; filename=%s' % filename

        # return response
class DownloadArchive(View):
    
    def get(self, request, *args, **kwargs):
        pass
        

"""

js
    fetch:
        /messages/retrieve/
        data: {latestPk: latestPk, threadPk: threadPk}
        success: console.log(data)
        latestPk

    fetch(latestPk, threadPk)

view
    Messages within the thread
    messages = filter pk__gt=latest_pk, thread_pk=thread
    build context; context['messages'] = []
    loop all message in messages:
       context['messages'].append({'pk': m.pk, 'content': m.content, 'when'...})
    return JsonResponse

js
longpolling
* setTimeout
    - fetch
    5000

longpolling w/ penalty
* setTimeout
    - fetch
    if data.objects.length === 0:
        penalize timerVAr + =
    5000

"""

