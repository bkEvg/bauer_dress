from notifications.models import Notification


def get_unread(request):
    qs = Notification.objects.unread()
    return {'get_unread': qs}
