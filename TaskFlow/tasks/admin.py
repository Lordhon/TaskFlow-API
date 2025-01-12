from django.contrib import admin

from tasks.models import UserProfile, Task

admin.site.register(UserProfile)
admin.site.register(Task)
