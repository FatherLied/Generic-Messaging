from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.http import HttpResponse
# Create your views here.
class WidgetView(TemplateView):
    template_name = 'widget/simpletemplate.html'

    def dispatch(self, request, *args, **kwargs):
        return super(WidgetView,self).dispatch(self.request, *args, **kwargs)