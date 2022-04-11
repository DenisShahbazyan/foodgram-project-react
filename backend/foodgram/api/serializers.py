from rest_framework import serializers

from recipes.models import Subscription, Tag, Ingredient, Recipe, AmountIngredientForRecipe
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        user = self.context['request'].user
        author = obj
        query = Subscription.objects.filter(user=author, author=user)
        if query:
            return True
        return False

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            del self.fields['is_subscribed']
        return data


class UserSetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        required=True
    )
    current_password = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ('new_password', 'current_password')


class GetTokenSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True
    )
    email = serializers.CharField(
        required=True
    )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


# class AmountIngredientForRecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AmountIngredientForRecipe
#         fields = ('id', 'recipe', 'ingredient', 'amount')


# class AddAmountForIngredientSerializer(IngredientSerializer):
#     amount = AmountIngredientForRecipeSerializer(read_only=True, many=True)

#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False

    # def validate(self, data):
    #     if self.context['request'].method == 'PUT':
    #         raise serializers.ValidationError('Запрос PUT запрещен!')
    #     return data
