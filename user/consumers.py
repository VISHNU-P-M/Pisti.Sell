from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'tester_message', 
                'tester':'how are you',
            }
        )
        
    def tester_message(self, event):
        tester = event['tester']
        async_to_sync(
            self.send(text_data=json.dumps({
                'tester':tester
            }))
        ) 
        
    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
