from django.conf.urls import url

from dashboard.views import ThreadDetailsView, AddNewThreadView, JoinThreadsView

urlpatterns = [
    url(r'^addnewthread/$', AddNewThreadView.as_view(), name='addnewthread'),
    url(r'^jointhreads/$', JoinThreadsView.as_view(), name='jointhreads'),
    url(r'^thread/(?P<pk>\d+)/$', ThreadDetailsView.as_view(), name='details')
]