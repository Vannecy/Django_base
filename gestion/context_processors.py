from .models import Messagerie

def unread_messages_count(request):
    unread_messages = Messagerie.objects.filter(recever=request.user, status='non lus')
    unread_messages_count = unread_messages.count()
    return {'unread_messages_count': unread_messages_count}