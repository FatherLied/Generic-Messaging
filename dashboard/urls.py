from django.conf.urls import url
from django.contrib.auth import views as auth_views
from dashboard import views as reg_views
from django.conf import settings

from dashboard.views import HomeView, SignUpView
from dashboard.views import ThreadDetailsView, AddNewThreadView, JoinThreadsView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', auth_views.login, 
        {'template_name': 'dashboard/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page':'login'}, name='logout'),
    url(r'^signup/$', reg_views.signup, name='signup'),

    url(r'^addnewthread/$', AddNewThreadView.as_view(), name='addnewthread'),
    url(r'^jointhreads/$', JoinThreadsView.as_view(), name='jointhreads'),
    url(r'^thread/(?P<pk>\d+)/$', ThreadDetailsView.as_view(), name='details')
]