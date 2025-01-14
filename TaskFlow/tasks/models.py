from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth.models import User as AuthUser


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('giver', 'Task Giver'),
        ('receiver', 'Task Receiver')
    )
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(choices=ROLE_CHOICES, max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10)
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_tasks' , null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_tasks',  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

