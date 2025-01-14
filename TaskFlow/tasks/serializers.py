from rest_framework import serializers
from .models import UserProfile, Task  # Импортируем свою кастомную модель User
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User as AuthUser
from rest_framework import serializers
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=['giver', 'receiver'], write_only=True, required=True)  # Указываем, что это write-only поле

    class Meta:
        model = AuthUser  # Используем стандартную модель User
        fields = ('username', 'password', 'email', 'role')

    def create(self, validated_data):
        # Создаем пользователя
        user = AuthUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        # Создаем профиль пользователя и сохраняем роль
        UserProfile.objects.create(user=user, role=validated_data['role'])
        return user


from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    giver = serializers.CharField(write_only=True, required=False)  # Делаем поле необязательным
    receiver = serializers.CharField(write_only=True, required=False)  # Это уже необязательное

    class Meta:
        model = Task
        fields = ('id','title', 'description', 'priority', 'giver', 'receiver', 'status' )

    def validate_giver(self, value):
        """Проверяем, что пользователь с таким username существует."""
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User with username {value} does not exist.")
        return user

    def validate_receiver(self, value):
        """Проверяем, что пользователь с таким username существует."""
        if value:  # Если receiver задан
            try:
                user = User.objects.get(username=value)
            except User.DoesNotExist:
                raise serializers.ValidationError(f"User with username {value} does not exist.")
            return user
        return None

    def to_representation(self, instance):
        """Добавляем детальную информацию о пользователе receiver."""
        representation = super().to_representation(instance)
        if instance.receiver:  # Проверяем, есть ли receiver
            representation['receiver_details'] = {
                'id': instance.receiver.id,
                'username': instance.receiver.username,
                'email': instance.receiver.email,
            }
        else:
            representation['receiver_details'] = None
        return representation

    def create(self, validated_data):
        """Создаем задачу и назначаем пользователей."""
        giver = validated_data.pop('giver')  # Это теперь объект User, а не ID
        receiver = validated_data.pop('receiver', None)  # Это также объект User, если он есть

        task = Task.objects.create(giver=giver, receiver=receiver, **validated_data)
        return task

