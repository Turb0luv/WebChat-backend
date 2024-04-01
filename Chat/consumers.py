import json

from channels.generic.websocket import WebsocketConsumer
from rest_framework.views import APIView

from .models import Message, User


class MessageConsumer(WebsocketConsumer, APIView):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        data = list(
            Message.objects.values().order_by('-created_at'))
        for date in data:
            date['created_at'] = date['created_at'].isoformat()
        to_send = json.dumps({
            'event': 'onmessage',
            'data': {
                'message': {
                    'type': 'connection',
                    'data': data,
        }}})
        self.send(text_data=to_send)

    # async def destroy_message(self, data):
    #     message = Message.objects.get(pk=data['message_id'])
    #     message.delete()
    #     await self.send_message(
    #         {'action': 'delete_message', 'message_id': data['message_id']})
    #
    # async def edit_message(self, data):
    #
    #     message = Message.objects.get(pk=data['message_id'])
    #     message.content = data['content']
    #     message.user_name = datetime.datetime.now()
    #     message.save()
    #     await self.send_message(
    #         {'action': 'edit_message', 'message': message.to_dict()})
    #
    def send_message(self, message):
        self.send(text_data=message)
