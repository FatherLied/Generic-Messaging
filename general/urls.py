from django.conf.urls import url, include
from django.contrib import admin

from dashboard.views import ThreadDetailsView, AddNewThreadView, JoinThreadsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^send/$', send_message, name='send_message')
    url(r'^',include('dashboard.urls')),
    url(r'^messenger/',include('messenger.urls')),
    url(r'^widget/', include('widget.urls'))
]

