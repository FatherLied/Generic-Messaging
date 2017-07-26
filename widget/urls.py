from django.conf.urls import url
from django.contrib.auth import views as auth_views
from dashboard import views as reg_views
from django.conf import settings


from .views import WidgetView, SignUpClientSiteView, Widget_UrlView

urlpatterns = [
    url(r'^w_template/$', WidgetView.as_view(), name='w_template'),
    url(r'^client_register/$', SignUpClientSiteView.as_view(), name='client_register'),
    url(r'^client_widget/$',Widget_UrlView.as_view(), name='widget_url' )
]