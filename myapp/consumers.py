# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VerseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        self.room_name = "verse_room"
        self.room_group_name = f"verse_{self.room_name}"

        # Join the WebSocket group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the WebSocket group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        book = text_data_json.get('book', '')
        chapter = text_data_json.get('chapter', '')
        versecount = text_data_json.get('versecount', '')

        # Send data to WebSocket group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'verse_update',
                'book': book,
                'chapter': chapter,
                'versecount': versecount,
            }
        )

    # Receive message from WebSocket group
    async def verse_update(self, event):
        book = event['book']
        chapter = event['chapter']
        versecount = event['versecount']

        # Send the updated verse details to WebSocket
        await self.send(text_data=json.dumps({
            'book': book,
            'chapter': chapter,
            'versecount': versecount,
        }))
