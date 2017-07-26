from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from dashboard.forms import SignUpForm
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from messenger.models import MessageThread, Message, Profile
from django.views import View

from braces.views import LoginRequiredMixin

"""
  AuthenticatedView just requires you to define:
    - template_name
    - http_method_names
    - get(), post(), etc.
    - get_context_data()
"""
class AuthenticatedView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    redirect_field_name = "Log-in"

    raise_exception = True
    redirect_unauthenticated_users = True

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
        
class HomeView(AuthenticatedView):
    template_name = 'dashboard/home.html'

    http_method_names = [
        'get'
    ]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or request.user.is_anonymous():
            return redirect(self.login_url)

        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        # context['users'] = Profile.objects.all().exclude(owner=self.request.user)
        context['threads'] = MessageThread.objects.filter(
            participants=self.request.user).order_by('-when_created')
        context['users'] = Profile.objects.all()
        context['allthreads'] = MessageThread.objects.exclude(
            participants=self.request.user)

        return context

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             user.save()
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'dashboard/signup.html', {'form': form})


class SignUpView(TemplateView):
    template_name = 'dashboard/signup.html'

    http_method_names = [
        'get',
        'post'
    ]

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context['form'] = SignUpForm()
        
        return context

    def post(self, request, *args, **kwargs):
        form = SignUpForm(self.request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(self.request, user)

            return redirect('home')

        return self.render_to_response({'form': form})

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)


class ThreadDetailsView(AuthenticatedView):
    template_name = 'dashboard/details.html'

    http_method_names = [
        'get'
    ]

    def get(self, request, pk):
        if not request.user.is_authenticated() or request.user.is_anonymous():
            return redirect(self.login_url)

        context = self.get_context_data(pk)
        return self.render_to_response(context)

    def get_context_data(self, pk):
        this_thread = get_object_or_404(MessageThread, pk=pk)

        if self.request.user not in this_thread.participants.all():
            raise Http404('Thread does not exist')

        context = {
            'threads':  MessageThread.objects.filter(
                participants=self.request.user).order_by('-when_created'),
            'users' : Profile.objects.all(),
            'thread_id': pk,
            'allthreads': MessageThread.objects.exclude(participants=self.request.user),
            'messages': Message.objects.filter(
                thread=this_thread).order_by('when_created'),
            'next_url': reverse('details', args=(pk,))
        }

        return context

class AddNewThreadView(AuthenticatedView):
    http_method_names = [
        'post'
    ]

    def post(self, request):
        subject = request.POST['subject']
        exists = MessageThread.objects.filter(subject=subject)
        if exists:
            return HttpResponse(' ')
        thread = MessageThread.objects.create(subject=subject)
        thread.participants.add(request.user)
        thread_url = reverse('details',args=(thread.pk,))
        return JsonResponse({'subject':thread.subject,'thread_url':thread_url})


class JoinThreadsView(AuthenticatedView):
    http_method_names = [
        'post'
    ]

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