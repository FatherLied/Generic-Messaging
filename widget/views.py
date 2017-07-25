
from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from dashboard.forms import SignUpForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from messenger.models import MessageThread, Message, Profile, Archive

from braces.views import LoginRequiredMixin

import time

# @method_decorator(login_required, name='dispatch')
class WidgetView(LoginRequiredMixin, TemplateView):

    template_name = 'widget/simpletemplate.html'

    login_url = "/login/"
    redirect_field_name = "Log-in"

    raise_exception = True
    redirect_unauthenticated_users = True

    http_method_names = [
        'get'
    ]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or request.user.is_anonymous():
            return redirect(self.login_url)

        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(WidgetView, self).get_context_data(**kwargs)
        context['users'] = Profile.objects.all().exclude(owner=self.request.user)

        return context

    def dispatch(self, request, *args, **kwargs):
       # return super(WidgetView,self).dispatch(self.request, *args, **kwargs)
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

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

       

