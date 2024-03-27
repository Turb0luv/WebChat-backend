import datetime
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import JsonResponse

from .models import Message


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data['command']
        #print(data)
        # if command == 'subscribe':
        #     await self.channel_layer.group_add(
        #         data['identifier'].split(',')
        #     )
        # if command == '':
        # #     await self.create_message(data)
        # # if command == 'create_message':
        # #     await self.create_message(data)
        # # elif command == 'destroy_message':
        # #     await self.destroy_message(data)
        # # elif command == 'edit_message':
        # #     await self.edit_message(data)
        # await self.send(json.dumps(Message.objects.all()))

    async def create_message(self, data):
        if data['content'] != '':
            message = Message.objects.create(user_id=data['user_id'],
                                             content=data['content'],
                                             user_name=data['user_name'],
                                             created_at=datetime.datetime.now())
            print(message)
            message.save()
            await self.send_message({'message': {'type': 'create', 'message': message.to.dict()}})

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
    async def send_message(self, message):
        await self.send(json.dumps(message))
