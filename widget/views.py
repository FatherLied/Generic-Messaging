from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from widget.models import MessageThread, Message
import time

class WidgetView(TemplateView):
    template_name = 'widget/simpletemplate.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetView, self).get_context_data(**kwargs)

        return context

    def dispatch(self, request, *args, **kwargs):
        return super(WidgetView,self).dispatch(self.request, *args, **kwargs)

class TestSiteView(TemplateView):
    template_name = 'widget/testsite.html'

    def get_context_data(self, **kwargs):
        context = super(TestSiteView, self).get_context_data(**kwargs)

        return context


class SendMessageView(View): 
    def post(self, request):
        content = request.POST.get('content')
        thread_id = request.POST.get('thread_id')
        thread = MessageThread.objects.get(pk=thread_id)
        message = Message.objects.add_message(content=content, 
            thread=thread, sender=request.user)
        date = message.when_created.strftime("%B %d, %Y, %-I:%M %p")
        return JsonResponse({'pk': message.pk,
            'threadId': message.thread_id, 
            'content': message.content, 
            'when': date, 
            'sender': message.sender.username, 
            'sender_pk': message.sender.pk
            })

class FetchMessage(View):

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

class AddNewThreadView(View):
    def post(self, request):
        subject = request.POST['subject']
        exists = MessageThread.objects.filter(subject=subject)
        if exists:
            return HttpResponse(' ')
        thread = MessageThread.objects.create(subject=subject)
        thread.participants.add('request.user')
        thread_url = reverse('simpletemplate',args=(thread.pk,))
        return JsonResponse({'subject':thread.subject,'thread_url':thread_url})


class JoinThreadsView(View):
    def post(self, request):
        subject = request.POST['subject']
        print(subject)
        thread = MessageThread.objects.get(subject=subject)
        thread1 = MessageThread.objects.filter(subject=subject).exclude(participants=request.user)
        if not thread:
            return JsonResponse({'status':'error1','context':'The thread does not exists.'})
        if not thread1:
            return JsonResponse({'status':'error2','context':'You are already part of the thread'})
        
        # thread = MessageThread.objects.filter(subject=subject)
        thread.participants.add(request.user)
        thread_url = reverse('simpletemplate',args=(thread.pk,))
        
        return JsonResponse({'subject':thread.subject,'thread_url':thread_url,'status':'success'})