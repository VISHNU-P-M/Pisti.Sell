from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import *

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        
    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self,text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        receiver_id = data['receiver_id']
        msgtype = data['type']
        author = CustomUser.objects.get(username=username) 
        if OneToOne.objects.filter(user1=author,user2_id=receiver_id).exists():
            pass
        elif OneToOne.objects.filter(user1=receiver_id,user2_id=author).exists():
            pass
        else:
            OneToOne.objects.create(user1=author,user2_id=receiver_id,room_name=self.room_name)
            
        if msgtype == 'image':
            print('image')
            pass
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msgtype':msgtype,
                'message': message,
                'username':username,
            }
        )
        
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        msgtype = event['msgtype']
        async_to_sync(
            self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'msgtype':msgtype
            }))
        )  