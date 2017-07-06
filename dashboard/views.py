from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from dashboard.forms import SignUpForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
	return render(request, 'dashboard/home.html')

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.save()
			password = form.cleaned_data.get('password1')
			user = authenticate(username = user.username, password = password)
			login(request, user)
			return redirect ('home')
	else:
		form = SignUpForm()
	return render(request, 'dashboard/signup.html', {'form': form})
