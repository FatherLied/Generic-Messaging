from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from dashboard.forms import SignUpForm

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from messenger.models import MessageThread, Message, Profile
from django.views import View

# # Create your views here.
# @login_required
# def home(request):
#     context = {
#         'threads': MessageThread.objects.filter(participants=request.user).order_by('-when_created'),
#         'users' : Profile.objects.all(),
#         'allthreads':MessageThread.objects.all().order_by('-when_created')
#     }
#     return render(request, 'dashboard/home.html',context = context)

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'dashboard/home.html'

    def dispatch(self, request, *args, **kwargs):
        return super(HomeView, self).dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['threads'] = MessageThread.objects.filter(participants=self.request.user).order_by('-when_created')
        context['users'] = Profile.objects.all()
        context['allthreads'] = MessageThread.objects.all().order_by('-when_created')

        return context

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

#===========================================

class SignUpView(TemplateView):
    template_name = 'dashboard/signup.html'
    form = SignUpForm()

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context['form'] = self.form
        
        return context

    def post(self, request, *args, **kwargs):
        self.form = SignUpForm(self.request.POST)
        if self.form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user = authenticate(username=user.username, password=password)
            login(self.request.user)

            return redirect('home')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

# def thread_details(request, pk):
#     thisthreads = get_object_or_404(MessageThread, pk=pk)
#     context = {
#         'threads': MessageThread.objects.filter(participants=request.user).order_by('-when_created'),
#         'users' : Profile.objects.all(),
#         'thisthreads':thisthreads,
#         'messages': Message.objects.filter(thread=thisthreads).order_by('when_created'),
#         'next_url': reverse('details', args=(pk,))
#     }
#     return render(request, 'dashboard/details.html', context=context)

class ThreadDetailsView(View):
    def dispatch(self, request, pk):
        thisthreads = get_object_or_404(MessageThread, pk=pk)
        context = {
            'threads':  MessageThread.objects.filter(participants=request.user).order_by('-when_created'),
            'users' : Profile.objects.all(),
            'thisthreads':thisthreads,
            'messages': Message.objects.filter(thread=thisthreads).order_by('when_created'),
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
        thread = get_object_or_404(MessageThread,subject=subject)
        thread.participants.add(request.user)
        thread_url = reverse('details',args=(thread.pk,))
        return JsonResponse({'subject':thread.subject,'thread_url':thread_url})