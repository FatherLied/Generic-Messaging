"""general URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from dashboard import views as reg_views
from dashboard.views import ThreadDetailsView, AddNewThreadView, JoinThreadsView
from messenger.views import AddMessageView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', reg_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'dashboard/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', reg_views.signup, name='signup'),

    url(r'^add/$', AddMessageView.as_view(), name='add_message'),
    url(r'^addnewthread/$', AddNewThreadView.as_view(), name='addnewthread'),
    url(r'^jointhreads/$', JoinThreadsView.as_view(), name='jointhreads'),
    url(r'^thread/(?P<pk>\d+)/$', ThreadDetailsView.as_view(), name='details'),
]

