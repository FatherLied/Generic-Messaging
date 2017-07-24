from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views import View

from messenger.models import MessageThread, Message, Profile
# Create your views here.

class WidgetView(TemplateView):
    template_name = 'widget/simpletemplate.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetView, self).get_context_data(**kwargs)
        context['users'] = Profile.objects.all().exclude(owner=self.request.user)

        return context

    def dispatch(self, request, *args, **kwargs):
        return super(WidgetView,self).dispatch(self.request, *args, **kwargs)

# class CreateMessageThread(View):
#     pass

# class MessageWidget(View):
#     def dispatch(self, request, pk):
#         thisthreads = get_object_or_404(MessageThread, pk=pk)
#         context = {
#             'messages': Message.objects.filter(
#                 thread=thisthreads).order_by('when_created'),
#             'next_url': reverse('details',args=(pk,))
#         }
#         return HttpResponse('')

# class AddMessageWidget(View):
#     def post(self, request):
#         w_content = request.POST.get('w_content')
#         w_thread_id = request.POST.get('w_thread_id')
#         thread = MessageThread.objects.get(pk=w_thread_id)
#         message = Message.objects.add_message(content=content,
#             thread=thread, sender=request.user)
#         return JsonResponse({
#             'threadId': message.thread_id,
#             'content': message.content,
#             'when': t,
#             'sender':message.sender.username,
#             'sender_pk': message.sender.pk
#             })

# class AllUsers(View):
#     def dispatch(self, request, pk):
#         users = Profile.objects.all()
#         return JsonResponse({'users':users})

# class RetrieveMessageWidget(View):

#     def get(self, request, *args, **kwargs):
#         latest_id = request.GET['latest_id']
#         thread_id = request.GET['threadId']
#         messages = Message.objects.filter(id__gt=latest_id,
#             thread__id=thread_id)
#         context = {}
#         context['messages'] = []
#         for message in messages:
#             context['messages'].append({'pk':message.pk,
#                 'content':message.content,
#                 'when':message.when_created.strtime("%B %d, %Y, %-I:%M %p"),
#                 'sender':message.sender.pk,
#                 'sender_pk':message.sender.pk})
#         return JsonResponse({'objects':context})
