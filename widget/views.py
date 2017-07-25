
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from widget.forms import RegisterForm


# Create your views here.
class WidgetView(TemplateView):
    template_name = 'widget/simpletemplate.html'

    def dispatch(self, request, *args, **kwargs):
        return super(WidgetView,self).dispatch(self.request, *args, **kwargs)

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