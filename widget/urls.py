from django.conf.urls import url
from django.contrib.auth import views as auth_views
from dashboard import views as reg_views
from django.conf import settings

from widget.views import WidgetView, SendMessageView, FetchMessage, TestSiteView, AddNewThreadView, JoinThreadsView

urlpatterns = [
    url(r'^w_template/$', WidgetView.as_view(), name='w_template'),
    url(r'^testsite/$', TestSiteView.as_view(), name='testsite'),
    url(r'^send_message/$', SendMessageView.as_view(), name='send_message'),
    url(r'^retrieve/$', FetchMessage.as_view(), name='retrieve-message'),
    url(r'^createnewthread/$', AddNewThreadView.as_view(), name='createnewthread'),
    url(r'^jointhreads/$', JoinThreadsView.as_view(), name='jointhreads')
]