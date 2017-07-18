from django.conf.urls import url

from .views import AddMessageView, RetrieveMessage

urlpatterns = [
    url(r'^add/$', AddMessageView.as_view(), name='add_message'),
    url(r'^retrieve/$', RetrieveMessage.as_view(), name='retrieve-message'),
]