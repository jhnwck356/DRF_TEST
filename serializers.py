from .models import Todo
from rest_framework import serializers
from django.contrib.auth.models import User

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            'Task_name','status','priority','remaining_days','desc','created_at','updated_at',
            )
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email','username', 'password',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user