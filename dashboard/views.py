from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from messenger.models import MessageThread, Message,Profile

def home(request):
	context = {
		'threads': MessageThread.objects.all().order_by('-when_created'),
		'users' : Profile.objects.all()
	}
	return render(request, 'dashboard/home.html', context = context)

def thread_details(request, pk):
	thisthreads = get_object_or_404(MessageThread, pk = pk)
	context = {
		'threads': MessageThread.objects.all().order_by('-when_created'),
		'users' : Profile.objects.all(),
		'thisthreads':thisthreads,
		'messages': Message.objects.filter(thread = thisthreads).order_by('when_created')
	}
	return render(request, 'dashboard/details.html', context = context)