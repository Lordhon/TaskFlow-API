from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics

from .permissions import IsGiver
from .serializers import RegisterSerializer, TaskSerializer
from .models import Task
from .utils import send_task_email_to_user

class CreateUserAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'User created successfully!'
        return response





class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsGiver, IsAuthenticated]
    queryset = Task.objects.all()
    def get_queryset(self):
        user = self.request.user  # Получаем текущего пользователя

        # Фильтруем задачи в зависимости от роли пользователя
        if user.profile.role == 'giver':
            # Если пользователь "giver", показываем только задачи, которые он создал
            return Task.objects.filter(giver=user)
        elif user.profile.role == 'receiver':
            # Если пользователь "receiver", показываем только задачи, где он назначен
            return Task.objects.filter(receiver=user)
        return Task.objects.none()  # Если роль не определена, ничего не возвращаем

    def perform_create(self, serializer):
        # Сохраняем задачу и назначаем текущего пользователя как giver
        task = serializer.save(giver=self.request.user)

        # Проверяем, что у задачи есть исполнитель (receiver) и что это не тот же пользователь, что и giver
        if task.receiver and task.receiver != task.giver:
            send_task_email_to_user(task.id)  # Отправляем email исполнителю