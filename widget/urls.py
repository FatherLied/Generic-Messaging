from django.conf.urls import url 

from .views import WidgetView, SignUpClientSiteView

urlpatterns = [
    url(r'^w_template/$', WidgetView.as_view(), name='w_template'),
    url(r'^client_register/$', SignUpClientSiteView.as_view(), name='client_register'),
]