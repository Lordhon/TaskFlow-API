import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "task_group"  # Создайте группу для задач

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отключаемся от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Обрабатываем сообщения, отправленные через WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Отправляем сообщение всем пользователям в группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'task_message',  # Название типа события
                'message': message
            }
        )

    async def task_message(self, event):
        # Получаем сообщение из события и отправляем его обратно пользователю через WebSocket
        message = event['message']

        # Отправляем сообщение через WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


