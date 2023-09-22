import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        other_username = self.scope["url_route"]["kwargs"]["username"]
        
        # Ensure the users are authenticated
        if not self.user.is_authenticated:
            await self.close()
        
        # Get the other user based on the username in the URL
        try:
            self.other_user = User.objects.get(username=other_username)
        except User.DoesNotExist:
            await self.close()

        # Create a unique room name for the chat (e.g., "chat_john_mary")
        self.room_name = f"chat_{self.user.username}_{self.other_user.username}"
        
        # Join the room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Send a message to the room group
        message_data = json.loads(text_data)
        message = message_data["message"]

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat.message",
                "message": message,
                "sender": self.user.username
            }
        )

    async def chat_message(self, event):
        # Send the message to the WebSocket
        message = event["message"]
        sender = event["sender"]

        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender
        }))
