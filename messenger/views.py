
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View
# Create your views here.
from .models import Message, MessageThread
from django.views import View
import time

# def add_message(request):
#     if request.method == "POST":
#         content = request.POST.get('content')
#         thread_id = request.POST.get('thread_id')
#         thread = MessageThread.objects.get(pk=thread_id)
#         message = Message.objects.add_message(content=content, thread=thread, sender=request.user)
#         return JsonResponse({'content': message.content, 'when': message.when_created.isoformat(), 'sender': message.sender.username})
#     return HttpResponse('')

class AddMessageView(View): 
    # def dispatch(self, request, **kwargs):
    #   if request.method is not 'POST':
    #     return HttpResponse('')
  
    def post(self, request): 
        print('Here')
        content = request.POST.get('content')
        print(request.POST.get('content'))
        thread_id = request.POST.get('thread_id')
        print(request.POST.get('thread_id'))
        thread = MessageThread.objects.get(pk=thread_id)
        message = Message.objects.add_message(content=content, thread=thread, sender=request.user)
        t = message.when_created.strftime("%B %d, %Y, %-I:%M %p")
        return JsonResponse({'pk': message.pk, 'content': message.content, 'when': t, 'sender': message.sender.username})


class RetrieveMessage(View):

    def get(self, request, *args, **kwargs):
        latest_id = request.GET['latestId']
        messages = Message.objects.filter(id__gt=latest_id)
        context = {}
        context['messages'] = []
        for message in messages:
            context['messages'].append({'pk': message.pk, 'content': message.content, 'when': message.when_created.isoformat(), 'sender': message.sender.username})
        return JsonResponse({'objects': context})
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

        

