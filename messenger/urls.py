from django.conf.urls import url

from .views import add_message, RetrieveMessage

urlpatterns = [
    url(r'^add/$', add_message, name='add_message'),
    url(r'^retrieve/$', RetrieveMessage.as_view(), name='retrieve-message'),
]