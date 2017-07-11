from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.
from .models import Message, MessageThread
from django.views import View

class AddMessage(View):

    def post(self, request):
        content = request.POST.get('content')
        thread_id = request.POST.get('thread_id')
        thread = MessageThread.objects.get(pk=thread_id)
        Message.objects.add_message(content=content, thread=thread, sender=request.user)
        return redirect(request.GET.get('next'))