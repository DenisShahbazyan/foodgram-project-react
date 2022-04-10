from rest_framework import serializers

from users.models import User
from recipes.models import Subscription


class UserListAndRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        i_am = self.context['request'].user
        author = obj

        print(i_am, '=', author)

        q = Subscription.objects.get(author=i_am)
        # Найти через User текущего пользователя, кто делает запрос
        # и через related_name обратиться к Subscription
        print(q)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            del self.fields['is_subscribed']
        return data


class GetTokenSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True
    )
    email = serializers.CharField(
        required=True
    )
