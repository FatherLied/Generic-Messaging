from django.conf.urls import url

from .views import AddMessageView, RetrieveMessage,ArchiveView,DownloadArchive

urlpatterns = [
    url(r'^add/$', AddMessageView.as_view(), name='add_message'),
    url(r'^retrieve/$', RetrieveMessage.as_view(), name='retrieve-message'),
    url(r'^archive/$', ArchiveView.as_view(), name='archive' ),
    url(r'^download_archive/$',DownloadArchive.as_view(), name='download_archive')
]