import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import User, Message
from .serializers import UserSerializer, LoginSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data['user'])
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data['user'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateMessageView(APIView):
    def post(self, request):
        if request.data['content'] != '':
            try:
                message = Message.objects.create(
                    user=User.objects.get(id=request.data['user_id']),
                    user_name=request.data['user_name'],
                    content=request.data['content'],
                    created_at=datetime.datetime.now())
                message.save()
                message_send = Message.objects.filter(id=message.id).values(
                    'id', 'content', 'user_name', 'user_id', 'created_at').last()
                message_send['created_at'] = message_send[
                    'created_at'].isoformat()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'Chat',
                    {
                        'type': 'create_message_frontend',
                        'message': message_send
                    })
                return Response(status=status.HTTP_201_CREATED)
            except Message.DoesNotExist:
                return Response(request.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(request.data, status=status.HTTP_204_NO_CONTENT)


class WorkMessageView(APIView):
    def delete(self, request, message_id):
        try:
            message = Message.objects.get(pk=message_id)
            message.delete()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'Chat',
                {
                    'type': 'send_updates',
                    'event': 'destroy'
                })
            return Response(request.data, status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, message_id):
        if request.data['content'] != '':
            try:
                message = Message.objects.get(pk=message_id)
                message.content = request.data['content']
                message.save()
                msg = {'id': message.id,
                       'user_id': request.data['user_id'],
                       'user_name': message.user_name,
                       'content': message.content,
                       'created_at': message.created_at}
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'Chat',
                    {
                        'type': 'send_updates',
                        'event': 'update'
                    })
                return Response(msg, status=status.HTTP_200_OK)
            except Message.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
