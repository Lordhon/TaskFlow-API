from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Task

def send_task_email_to_user(task_id):
    task = get_object_or_404(Task, id=task_id)#поиск задачи по id task иначе 404

    if task.receiver:
        recipient_email = task.receiver.email  # Получаем email

        subject = f"New Task: {task.title}"
        message = f"""
        Тебе пришла задача:
        Title: {task.title}
        Priority: {task.priority}
        Description: {task.description}

        Пожалуйста, войдите в систему, чтобы выполнить задание.
        """


        # Отправляем email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email], fail_silently=False)


