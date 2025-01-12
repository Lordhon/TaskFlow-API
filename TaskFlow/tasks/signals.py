from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(pre_save, sender=Task)
def notify_status_change(sender, instance, **kwargs):
    if instance.id:  # Если задача уже существует (обновление)
        old_instance = Task.objects.get(id=instance.id)
        if old_instance.status != instance.status:  # Если статус изменился
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{instance.receiver.id}",
                {
                    "type": "task_status_notification",
                    "message": f"Task '{instance.title}' updated to {instance.status}"
                }
            )