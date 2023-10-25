import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User, Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get user IDs from URL route
        self.first_user_id = self.scope["url_route"]["kwargs"]["first_user_id"]
        self.second_user_id = self.scope["url_route"]["kwargs"]["second_user_id"]

        # Authenticate and authorize the user
        self.first_user = await self.get_user(self.first_user_id)
        self.second_user = await self.get_user(self.second_user_id)

        if not self.first_user or not self.second_user:
            self.close()
            return

        self.room_name = f"chat_{self.first_user_id}_{self.second_user_id}"

        # Add both users to the same room
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the chat room when they disconnect
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        # Receive a message and send it to the other user
        text_data_json = json.loads(text_data)
        message = text_data_json["content"]
        sender = text_data_json["sender"]

        try:
            sender_user = await self.get_user(sender)
            await self.save_message(sender_user, message)
            
            # Notify the other user about the new message
            recipient_id = self.first_user_id if sender_user == self.second_user else self.second_user_id
            await self.notify_new_message(recipient_id, message, sender_user.first_name)
            
            # Send the message to the chat room
            await self.channel_layer.group_send(
                self.room_name,
                {"type": "chat.message", "message": message, "sender": sender_user.id},
            )
        except User.DoesNotExist:
            print("User does not exist")
        except Exception as e:
            print("Something went wrong", e)

    async def chat_message(self, event):
        # Send the message to the WebSocket client
        message = event["message"]
        sender = event["sender"]
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))

    @database_sync_to_async
    def get_user(self, user_id):
        # Retrieve a user based on their ID
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, sender, message_content):
        # Save the message to the database
        chat, _ = Chat.objects.get_or_create(sender=sender, receiver=self.second_user)
        Message.objects.create(chat=chat, sender=sender, content=message_content)
    
    async def notify_new_message(self, recipient_id, message_content, sender_name):
        # Notify the recipient about the new message
        await self.channel_layer.group_send(
            f"notifications_user_{recipient_id}",
            {
                "type": "notification.new_message",
                "message": message_content,
                "sender_name": sender_name,
            },
        )
        print("notiiiiiiiiiiiiiiiiiiiiiiiiiiiiiif sent")



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if user.is_authenticated:
            await self.accept()
            user_id = user.id
            await self.channel_layer.group_add(f"notifications_user_{user_id}", self.channel_name)

    async def disconnect(self, close_code):
        user = self.scope["user"]

        if user.is_authenticated:
            user_id = user.id
            await self.channel_layer.group_discard(f"notifications_user_{user_id}", self.channel_name)

    async def receive(self, text_data):
        # Handle incoming messages if needed (for notifications)
        pass

    async def notification_new_message(self, event):
        # Send a notification about a new message to the WebSocket client
        message = event["message"]
        sender_name = event["sender_name"]
        await self.send(text_data=json.dumps({
            "type": "new_message",
            "message": message,
            "sender_name": sender_name,
        }))