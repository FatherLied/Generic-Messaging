from django.conf.urls import url 

from .views import WidgetView

urlpatterns = [
    url(r'^w_template/$', WidgetView.as_view(), name='w_template'),
]