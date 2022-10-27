from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from api.models import Image, Task


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TaskImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    
    class Meta:
        model = Task
        fields = '__all__'


class TaskSerializerExecutor(TaskSerializer):
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    
    class Meta:
        model = Task
        fields = ('status',)
    
    def update(self, instance, validated_data):
        print(validated_data)
        instance.status = validated_data.get("status", instance.status)
        if instance.status in ('N', 'C'):
            print("PermissionDenied")
            raise PermissionDenied({"detail": "You can specify the status only from 'New task' to 'In Progres'"})
        instance = super(TaskSerializerExecutor,self).update(instance, validated_data)

        return instance


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
