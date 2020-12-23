from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # User содержит много полей, exclude получается слишком длинным
        # Перечисляем только нужные
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
