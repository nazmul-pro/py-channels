# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import jwt, json
from testapp.models import AppUser, LiveDiscussion, AppUserToken

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        print('connected', self)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'live_discussion_exam'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("-----------")
        print(self.room_group_name, self.channel_name)
        print("-----------")

        await self.accept()

        # send prev msg
        prev = LiveDiscussion.objects.all()
        if prev:
            for chat in prev:
                c_text = chat.text
                c_user_id = chat.app_user.id
                print(c_text, c_user_id)
                await self.send(text_data=json.dumps({
                    'message': c_text,
                    'user_id': c_user_id
                }))

    async def disconnect(self, close_code):
        # Leave room group
        print('disconnected', self)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        token = text_data_json['taka']
        if not token:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        else:
            v_user = AppUserToken.objects.filter(jwt=token).get()
            if v_user:
                print(v_user)
                message = text_data_json['message']
                # Save the msg in db
                # make user Obj by Token
                user_info = jwt.decode(token, "SECRET_KEY")
                print("user", user_info)
                # create fake user instance
                user = AppUser(id=user_info['app_user'], name="demo", email="demo")
                
                chat = LiveDiscussion(app_user=user, text=message, love=0)
                chat.save()

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'user_id': v_user.app_user_id
                    }
                )
                
        

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        print('got event', event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': event['user_id']
        }))