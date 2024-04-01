import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message


class MessageConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "Chat"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            'Chat',
            {
                'type': 'send_updates',
                'event': 'connection'
            })

    def create_message_frontend(self, event):
        message = event['message']
        to_send = json.dumps({
            'event': 'onmessage',
            'data': {
                'message': {
                    'type': 'create',
                    'data': message,
                }}})
        self.send(text_data=to_send)

    def send_updates(self, event):
        event = event['event']
        data = list(
            Message.objects.values('id', 'content', 'user_id',
                                   'created_at').order_by('created_at'))
        for date in data:
            date['created_at'] = date['created_at'].isoformat()
        to_send = json.dumps({
            'event': event,
            'data': {
                'message': {
                    'type': 'connection',
                    'data': data,
                }}})
        self.send(text_data=to_send)
