from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.
from .models import Message, MessageThread

def add_message(request):
    if request.method == "POST":
        content = request.POST.get('content')
        thread_id = request.POST.get('thread_id')
        thread = MessageThread.objects.get(pk=thread_id)
        message = Message.objects.add_message(content=content, thread=thread, sender=request.user)
        return JsonResponse({'content': message.content, 'when': message.when_created.isoformat(), 'sender': message.sender.username})
    return HttpResponse('')
# def send_message(request):

#     if request.method == "POST":
#         content = request.POST.get('content')
#         thread_id = request.POST.get('thread_id')
#         thread = MessageThread.objects.get(pk=thread_id)
#         Message.objects.add_message(content=content, thread=thread, sender=request.user)
#     print (request.POST.get('content'))
#     return HttpResponse('')
  


