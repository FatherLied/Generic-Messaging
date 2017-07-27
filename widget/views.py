
from django.views.generic.base import TemplateView
from django.views import View
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from dashboard.forms import SignUpForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from messenger.models import MessageThread, Message, Profile, Archive, SiteProfile

from braces.views import LoginRequiredMixin
from widget.forms import RegisterForm
import time, os, base64
from django.core import signing

# from dashboard.views import AuthenticatedView

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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get(self, request, *args, **kwargs):
        access_key = request.GET.get('access_key')
        print(access_key)
        # return HttpResponse('Hallo')
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(Widget_UrlView, self).get_context_data(**kwargs)
        return context

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
