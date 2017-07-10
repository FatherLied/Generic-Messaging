from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from dashboard.forms import SignUpForm
from django.contrib.auth.decorators import login_required
from messenger.models import MessageThread, Message, Profile

# Create your views here.
@login_required
def home(request):
    context = {
        'threads': MessageThread.objects.all().order_by('-when_created'),
        'users' : Profile.objects.all()
    }
    return render(request, 'dashboard/home.html', context=context)

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

def thread_details(request, pk):
    thisthreads = get_object_or_404(MessageThread, pk=pk)
    context = {
        'threads': MessageThread.objects.all().order_by('-when_created'),
        'users' : Profile.objects.all(),
        'thisthreads':thisthreads,
        'messages': Message.objects.filter(thread=thisthreads).order_by('when_created'),
        'next_url': reverse('details', args=(pk,))
    }
    return render(request, 'dashboard/details.html', context=context)