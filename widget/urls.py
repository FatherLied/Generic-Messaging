from django.conf.urls import url 

from .views import WidgetView, ClientView

urlpatterns = [
    url(r'^w_template/$', WidgetView.as_view(), name='w_template'),
    url(r'^client/$', ClientView.as_view(), name='client'),
]