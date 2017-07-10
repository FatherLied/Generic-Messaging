from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.
from .models import Message, MessageThread

def add_message(request):
    redirect_url = request.GET.get('next')
    if redirect_url is None:
        redirect_url = '/'
    if request.method == "POST":
        content = request.POST.get('content')
        thread_id = request.POST.get('thread_id')
        thread = MessageThread.objects.get(pk=thread_id)
        Message.objects.add_message(content=content, thread=thread, sender=request.user)
    return redirect(redirect_url)

