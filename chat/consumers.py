# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name


        print("self.channel_name",self.channel_name)
        print(" self.room_name ", self.room_name )
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):

        print("disconnect",self.room_group_name,"  ",self.channel_name)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("recive message",text_data)
        
        fetchdata = users.objects.all().values('id','name')
        
        finalarray = list()
        for j in fetchdata:
            finalarray.append({'id':j['id'],'name':j['name']})



        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'data':finalarray
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        data = event['data']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data':data
        }))





class Notification(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notification_%s' % self.room_name

        print("notification")
        print("self.channel_name",self.channel_name)
        print(" self.room_name ", self.room_name )
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()



    def disconnect(self, close_code):

        print("disconnect",self.room_group_name,"  ",self.channel_name)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    def receive(self, text_data):
        print("recive message",text_data)
        
        fetchdata = users.objects.all().values('id','name')
        
        finalarray = list()
        for j in fetchdata:
            finalarray.append({'id':j['id'],'name':j['name']})



        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'notification_message',
                'message': message,
                'data':finalarray
            }
        )

    # Receive message from room group
    def notification_message(self, event):
        message = event['message']
        data = event['data']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data':data
        }))
