from django.contrib.auth import get_user_model
from djoser import serializers as djoser_serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from recipes.models import (AmountIngredientForRecipe, Ingredient, Recipe,
                            Subscription, Tag)

User = get_user_model()


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name',
                  'last_name')


class UserSerializer(djoser_serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj.id).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientForRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = AmountIngredientForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ListRetrieveRecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = AmountIngredientForRecipeSerializer(
        source='amountingredientforrecipe', many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    # TODO доделать для авторизованного пользователя
    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return False

    # TODO доделать для авторизованного пользователя
    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return False

    def create(self, validated_data):
        user = self.context['request'].user

        tags_data = validated_data.pop('tags')
        tags = []
        for id in tags_data:
            tag = get_object_or_404(Tag, id=id)
            tags.append(tag)

        ingredients_data = validated_data.pop('ingredients')
        ingredients = []
        recipe = Recipe(author=user, **validated_data)
        recipe.save()
        for field in ingredients_data:
            ingredient = get_object_or_404(Ingredient, id=field['id'])
            AmountIngredientForRecipe.objects.create(
                recipe=recipe, ingredient=ingredient, amount=field['amount']
            )
            ingredients.append(ingredient)

        recipe.tags.add(*tags)
        recipe.ingredients.add(*ingredients)
        return recipe


class AmountWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class CreateUpdateDestroyRecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = AmountWriteSerializer(many=True)
    tags = serializers.ListField()
    image = Base64ImageField()
    name = serializers.CharField(max_length=200)
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def to_representation(self, instance):
        return ListRetrieveRecipeSerializer(instance,
                                            context=self.context).data

    def create(self, validated_data):
        user = self.context['request'].user

        tags_data = validated_data.pop('tags')
        tags = []
        for id in tags_data:
            tag = get_object_or_404(Tag, id=id)
            tags.append(tag)

        ingredients_data = validated_data.pop('ingredients')
        ingredients = []
        recipe = Recipe(author=user, **validated_data)
        recipe.save()
        for field in ingredients_data:
            ingredient = get_object_or_404(Ingredient, id=field['id'])
            AmountIngredientForRecipe.objects.create(
                recipe=recipe, ingredient=ingredient, amount=field['amount']
            )
            ingredients.append(ingredient)

        recipe.tags.add(*tags)
        recipe.ingredients.add(*ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.get("ingredients")
        ingredients = []
        for field in ingredients_data:
            ingredient = get_object_or_404(Ingredient, id=field['id'])
            AmountIngredientForRecipe.objects.filter(
                recipe=instance
            ).update_or_create(
                recipe=instance, ingredient=ingredient,
                amount=field['amount']
            )
            ingredients.append(ingredient)

        instance.ingredients.set(ingredients)
        instance.tags.set(validated_data.get('tags'))
        instance.image = validated_data.get('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.save()
        return instance


class SimpleRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(UserSerializer):
    recipes = SimpleRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class CurrentAuthorDefault:
    requires_context = True

    def __call__(self, serializer_field):
        author_id = serializer_field.context['request'].parser_context[
            'kwargs']['author_id']
        return get_object_or_404(User, id=author_id)


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.HiddenField(default=CurrentAuthorDefault())
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    # is_subscribed = serializers.ReadOnlyField(source='get_is_subscribed')

    class Meta:
        model = Subscription
        # fields = ('is_subscribed', 'recipes', 'recipes_count')
        fields = ('user', 'author', 'email', 'id', 'username', 'first_name',
                  'last_name')
