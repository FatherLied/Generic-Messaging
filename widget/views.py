from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from messenger.models import MessageThread, Message, Profile, ProfileThread
import time


class WidgetView(TemplateView):
    template_name = 'widget/simpletemplate.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetView, self).get_context_data(**kwargs)

        return context

    def dispatch(self, request, *args, **kwargs):
        return super(WidgetView, self).dispatch(self.request, *args, **kwargs)


class TestSiteView(TemplateView):
    template_name = 'widget/testsite.html'

    def get_context_data(self, **kwargs):
        context = super(TestSiteView, self).get_context_data(**kwargs)

        return context


class SendMessageView(View): 
    def post(self, request):
        content = request.POST.get('content')
        thread_id = request.POST.get('thread_id')
        ip_address = request.POST.get('ip')
        if request.user.is_anonymous():
            user = User.objects.get(profile__ip_address=ip_address)
        else:
            user = request.user
        thread = MessageThread.objects.get(pk=thread_id)
        message = Message.objects.add_message(content=content, 
            thread=thread, sender=user)
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
                'sender_pk': message.sender.pk
                })
        return JsonResponse({'objects': context})

class AddNewThreadView(View):
    def post(self, request):
        subject = request.POST['subject']
        ip_address = request.POST['ip']
        user_anonymous = None
        if request.user.is_anonymous() and not User.objects.filter(username=ip_address).exists():
            user_anonymous = User.objects.create_user(username=ip_address, password=ip_address)
            user_anonymous.profile.ip_address = ip_address
            user_anonymous.profile.save()
        threads = MessageThread.objects.filter(subject=subject)

        if threads:
            thread = threads.first()
            messages = Message.objects.filter(thread=thread)
            context = {}
            context['messages'] = []
            for message in messages:
                context['messages'].append({'pk': message.pk, 
                    'content': message.content, 
                    'when': message.when_created.strftime("%B %d, %Y, %-I:%M %p"),
                    'sender': message.sender.username, 
                    'sender_pk': message.sender.pk
                    })
            return JsonResponse({'thread_id':thread.id, 'objects':context})
        thread = MessageThread.objects.create(subject=subject)
        thread.participants.add(user_anonymous)
        return JsonResponse({'thread_id':thread.id})

class ThreadDetailsView(View):
    def dispatch(self, request, pk):
        thisthreads = get_object_or_404(MessageThread, pk=pk)
        context = {
            'threads':  MessageThread.objects.filter(
                participants=request.user).order_by('-when_created'),
            'users' : Profile.objects.all(),
            'thread_id':pk,
            'allthreads':MessageThread.objects.exclude(participants=request.user),
            'messages': Message.objects.filter(
                thread=thisthreads).order_by('when_created'),
            'next_url': reverse('details', args=(pk,))
        }
        return render(request, 'widget/details.html', context=context)