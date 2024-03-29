
from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from dashboard.forms import SignUpForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from messenger.models import MessageThread, Message, Profile, Archive, SiteProfile
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
from widget.forms import RegisterForm
import time, os, base64
import string
from django.core import signing

# from dashboard.views import AuthenticatedView

class WidgetView(TemplateView):
    template_name = 'widget/simpletemplate.html'

    def get_context_data(self, request, *args, **kwargs):
        context = super(WidgetView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        access_key = request.GET.get('access_key')
        print(access_key)
        site = SiteProfile.objects.filter(access_key=access_key)
        if not site:
            return HttpResponse('wrong access key')
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

        try:
            thread = MessageThread.objects.get(pk=thread_id)
        except MessageThread.DoesNotExist:
            thread = MessageThread.objects.create(subject=ip_address)
            thread.participants.add(user)

        message = Message.objects.add_message(content=content,
            thread=thread, sender=user)
        date = message.when_created.strftime("%B %d, %Y, %-I:%M %p")
        if user != request.user:
            return JsonResponse({'pk': message.pk,
                'threadId': message.thread_id,
                'content': message.content,
                'when': date,
                'sender': 'You',
                'sender_pk': message.sender.pk,
                'hello': ip_address
                })

        return JsonResponse({'pk': message.pk,
            'threadId': message.thread_id,
            'content': message.content,
            'when': date,
            'sender': message.sender.username,
            'sender_pk': message.sender.pk,
            'hello': ip_address
            })

class FetchMessage(View):

    def get(self, request, *args, **kwargs):
        latest_id = request.GET['latestId']
        thread_id = request.GET['threadId']
        ip_address = request.GET['ip']
        messages = Message.objects.filter(id__gt=latest_id, thread__id=thread_id)
        context = {}
        context['messages'] = []
        for message in messages:
            if message.sender.username == ip_address:
                context['messages'].append({'pk': message.pk,
                    'content': message.content,
                    'when': message.when_created.strftime("%B %d, %Y, %-I:%M %p"),
                    'sender': 'You',
                    'sender_pk': message.sender.pk
                    })
            else:
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
        access_key = request.POST['access_key']
        print(access_key)
        user_anonymous = None
        if request.user.is_anonymous() and not User.objects.filter(username=ip_address).exists():
            user_anonymous = User.objects.create_user(username=ip_address, password=ip_address)
            user_anonymous.profile.ip_address = ip_address
            user_anonymous.profile.save()
        else:
            user_anonymous = User.objects.get(username=ip_address)
        threads = MessageThread.objects.filter(subject=subject)
        context = {}
        context['messages'] = []
        if threads:
            thread = threads.first()
            messages = Message.objects.filter(thread=thread)
            for message in messages:
                if message.sender.username == ip_address:
                    context['messages'].append({'pk': message.pk,
                        'content': message.content,
                        'when': message.when_created.strftime("%B %d, %Y, %-I:%M %p"),
                        'sender': 'You',
                        'sender_pk': message.sender.pk
                        })
                else:
                    context['messages'].append({'pk': message.pk,
                            'content': message.content,
                            'when': message.when_created.strftime("%B %d, %Y, %-I:%M %p"),
                            'sender': message.sender.username,
                            'sender_pk': message.sender.pk
                            })

            return JsonResponse({'thread_id':thread.id, 'objects':context})
        thread = MessageThread.objects.create(subject=subject,status='PE')
        site = SiteProfile.objects.filter(access_key=access_key)
        print(site[0].owner)
        thread.participants.add(user_anonymous)
        thread.participants.add(site[0].owner)
        return JsonResponse({'thread_id':thread.id,'objects':context})

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

class SignUpClientSiteView(TemplateView):
    template_name = 'widget/client.html'
    form = RegisterForm()

    def get_context_data(self, **kwargs):
        context = super(SignUpClientSiteView, self).get_context_data(**kwargs)
        context['form'] = self.form 
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(self.request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            web_domain = form.cleaned_data['web_domain']
            domain = SiteProfile.objects.filter(domain=web_domain)
            if domain:
                return HttpResponse('That domain is already registered.')

            access_secret = base64.b64encode(os.urandom(50)).decode('ascii')
            access_key = signing.dumps(access_secret)[0:(len(access_secret))]
            SiteProfile.objects.create(domain=web_domain, access_secret=access_secret, 
                company_name=company_name, owner=request.user, access_key=access_key)
            # return JsonResponse({'access_key':access_key, 'access_secret': access_secret})
            return redirect('/')

class Widget_UrlView(TemplateView):
    template_name = "widget/simpletemplate.html"
    http_method_names = [
        'get'
    ]

    def get(self, request, *args, **kwargs):
        access_key = request.GET.get('access_key')
        print(access_key)
        self.access_key = access_key
        # return HttpResponse('Hallo')
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(Widget_UrlView, self).get_context_data(**kwargs)
        context['access_key'] = self.access_key
        return context

    def dispatch(self, request, *args, **kwargs):
        # return super(WidgetView,self).dispatch(self.request, *args, **kwargs)
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        super(AuthenticatedView, self).http_method_not_allowed(request)
        raise Http404
