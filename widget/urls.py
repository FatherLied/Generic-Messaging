from django.conf.urls import url 

from .views import WidgetView 
#,MessageWidget, AddMessageWidget, AllUsers, 
# RetrieveMessageWidget

urlpatterns = [
    url(r'^home/$', WidgetView.as_view(), name='w_template'),
    # url(r'^messagewidget/$', MessageWidget.as_view(),name=messagewidget),
    #url(r'^addmessage/$' AddMessageWidget.as_view(), name=addmessagewidget).
    #url(r'^allusers/$', AllUsers.as_view(), name='allusers'),
    #url(r'^retrivemessage/$', RetrieveMessageWdget.as_view(), name='retrieve')
]