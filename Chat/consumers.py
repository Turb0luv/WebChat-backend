import json

from channels.generic.websocket import WebsocketConsumer

from .models import Message


class MessageConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        self.send_updates('connection')

    def send_updates(self, event):
        data = list(
            Message.objects.values().order_by('-created_at'))
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
