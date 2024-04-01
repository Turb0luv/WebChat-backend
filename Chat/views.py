import datetime
import json

from channels.generic.websocket import WebsocketConsumer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .consumers import MessageConsumer
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
                    'id', 'content', 'user', 'created_at').last()
                message_send['created_at'] = message_send['created_at'].isoformat()
                print(message_send)
                to_send = json.dumps({
                    'event': 'onmessage',
                    'data': {
                        'message': {
                            'type': 'create',
                            'data': message_send,
                        }}})
                #Тут надо вызвать send WebsocketConsumer'a
                print(to_send)
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
            # Тут надо вызвать send_update WebsocketConsumer'a
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, message_id):
        try:
            message = Message.objects.get(pk=message_id)
            message.content = request.data['content']
            message.save()
            return Response(request.data, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

