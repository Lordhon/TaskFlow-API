Проект представляет собой систему, основанную на ролях, где пользователи могут быть разделены на две категории: giver и receiver. Giver (тот, кто выдает задачи) назначает задачи receiver (получателю), и задачи отправляются на почту получателя. Для авторизации пользователей используется JWT-токен. Также реализован общий чат асинхронный с помощью websocket для общения между giver и receiver, где они могут обмениваться информацией о задачах.
