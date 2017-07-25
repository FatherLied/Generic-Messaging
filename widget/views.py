from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from dashboard.forms import SignUpForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from messenger.models import MessageThread, Message, Profile, Archive

import time

@method_decorator(login_required, name='dispatch')
class WidgetView(TemplateView):
    template_name = 'widget/simpletemplate.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetView, self).get_context_data(**kwargs)
        context['users'] = Profile.objects.all().exclude(owner=self.request.user)

        return context

    def dispatch(self, request, *args, **kwargs):
        return super(WidgetView,self).dispatch(self.request, *args, **kwargs)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'dashboard/signup.html', {'form': form})


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
        return render(request, 'dashboard/details.html', context=context)

class AddNewThreadView(View):
    def post(self, request):
        subject = request.POST['subject']
        exists = MessageThread.objects.filter(subject=subject)
        if exists:
            return HttpResponse(' ')
        thread = MessageThread.objects.create(subject=subject)
        thread.participants.add(request.user)
        thread_url = reverse('details',args=(thread.pk,))
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
        thread_url = reverse('details',args=(thread.pk,))
        
        return JsonResponse({'subject':thread.subject,'thread_url':thread_url,'status':'success'})

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