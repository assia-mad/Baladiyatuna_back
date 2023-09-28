import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User, Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect websockets")
        self.first_user_id = self.scope["url_route"]["kwargs"]["first_user_id"]
        self.second_user_id = self.scope["url_route"]["kwargs"]["second_user_id"]

        #check if users exists
        self.first_user = await self.get_user(self.first_user_id)
        self.second_user = await self.get_user(self.second_user_id)
        if not self.first_user or not self.second_user:
            print("no users§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§")
            self.close()

        self.chat = await self.get_or_create_chat(self.first_user,self.second_user)
        self.room_name = (
            f"chat_{self.chat.id}"
        )
        self.room_group_name = f"chat_group_{self.chat.id}"                           
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        print("receiiiiiiiiiiiiiving the message")
        text_data_json = json.loads(text_data)
        print('done1')
        message = text_data_json["content"]
        print("done2",message)
        sender = text_data_json["sender"]
        print("done3",sender)

        try:
 
            sender_user = await self.get_user(sender)
            print("dooooooooooone")
            await self.save_message(message,sender_user)
            await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "sender":sender_user}
        )
        except User.DoesNotExist:
            print("user does not exist")
        except Exception as e:
         print("something go wrong",e)
        



    async def chat_message(self, event):
        print("sending the messageeeeeeeeeeeeeeeeee")
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_or_create_chat(self, sender, receiver):
        chat, created = Chat.objects.get_or_create(
            sender=sender, receiver=receiver
        )
        return chat
    
    @database_sync_to_async
    def save_message(self, content, sender):
        print("saving the message to BDD"    , self.chat, sender, content)
        Message.objects.create(chat=self.chat, sender=sender, content=content)
        print("saved")
