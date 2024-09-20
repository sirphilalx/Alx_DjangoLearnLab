from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')
    notifications_data = [{
        "actor": notification.actor.username,
        "verb": notification.verb,
        "target": str(notification.target),
        "timestamp": notification.timestamp
    } for notification in notifications]

    return Response(notifications_data, status=status.HTTP_200_OK)