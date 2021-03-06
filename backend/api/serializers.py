from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser import serializers as djoser_serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import AmountIngredientForRecipe, Ingredient, Recipe, Tag

User = get_user_model()


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    """Сериализатор для создания новго пользователя. Модель User.
    """

    class Meta:
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name',
                  'last_name')


class UserSerializer(djoser_serializers.UserSerializer):
    """Сериализатор для работы с пользователями. Модель User.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Возвращает подписан ли текущий пользователь на автора.

        Returns:
            True: Подписан.
            False: Не подписан.
        """
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с тегами. Модель Tag.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с ингоедиентами. Модель Ingredient.
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientForRecipeSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для отображения количества ингредиента в
    запросе рецептов. Модель AmountIngredientForRecipe.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredientForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ListRetrieveRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка рецептов, и конкретного рецепта.
    Модель Recipe.
    """
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = AmountIngredientForRecipeSerializer(
        source='amountingredientforrecipes', many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        """Возвращает добавлен ли рецепт в избранное.

        Returns:
            True: Рецепт есть в избранном.
            False: Рецепта нет в избранном.
        """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe_id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Возвращает добавлен ли рецепт в список покупок.

        Returns:
            True: Рецепт есть в списке покупок.
            False: Рецепта нет в списке покупок.
        """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_carts.filter(recipe_id=obj.id).exists()


class AmountWriteSerializer(serializers.Serializer):
    """Вспомогательный сериализатор для добавления рецептов. Для добавления
    количества конкретного ингредиента и его количества в рецепт.
    """
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class CreateUpdateDestroyRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления, изменения, удаления рецепта.
    """
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
        return ListRetrieveRecipeSerializer(
            instance, context=self.context
        ).data

    def validate(self, data):
        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': ('Выберите ингредиенты')
            })

        min_amount_ingredient = 1
        max_amount_ingredient = 1000

        unique_ingredients = []
        for ingredients_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=(ingredients_item['id']))
            if ingredient in unique_ingredients:
                raise serializers.ValidationError('Ингредиенты должны '
                                                  'быть уникальными')
            unique_ingredients.append(ingredient)

            if int(ingredients_item['amount']) < min_amount_ingredient:
                raise serializers.ValidationError({
                    'ingredients': ('Минимальное количество ингредиента '
                                    f'{min_amount_ingredient}')
                })
            if int(ingredients_item['amount']) > max_amount_ingredient:
                raise serializers.ValidationError({
                    'ingredients': ('Максимальное количество ингредиента '
                                    f'{max_amount_ingredient}')
                })

        cooking_time = data.get('cooking_time')
        if not cooking_time:
            raise serializers.ValidationError({
                'cooking_time': ('Введите время готовки')
            })

        min_cooking_time = 1
        max_cooking_time = 24 * 60

        if int(cooking_time) < min_cooking_time:
            raise serializers.ValidationError({
                'cooking_time': ('Минимальное время приготовления 1 минута')
            })
        if int(cooking_time) > max_cooking_time:
            raise serializers.ValidationError({
                'cooking_time': ('Максимальное время приготовления сутки '
                                 f'({max_cooking_time} минут))')
            })

        return data

    def create_amount_ingredient_for_recipe(self, recipe, ingredients):
        """Записывает ингредиенты вложенные в рецепт.
        Создает объект AmountIngredientForRecipe.
        """
        for ingredient in ingredients:
            AmountIngredientForRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
            )

    def create(self, validated_data):
        """Создает рецепт.
        """
        user = self.context['request'].user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags_data)
        self.create_amount_ingredient_for_recipe(recipe, ingredients_data)
        return recipe

    def update(self, recipe, validated_data):
        """Обновляет рецепт.
        """
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)

        if ingredients_data:
            recipe.amountingredientforrecipes.all().delete()
            self.create_amount_ingredient_for_recipe(recipe, ingredients_data)

        recipe.save()
        return super().update(recipe, validated_data)


class SimpleRecipeSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор вывода рецептов в подписках.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(UserSerializer):
    """Сериализатор для работы с подписками.
    """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(
        source='recipes.count',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_recipes(self, obj):
        """Возвращет рецепты авторов при запросе авторов, на которых подписан
        текущий пользователь.

        Params:
            recipes_limit: сколько рецептов выодить у автора.
        """
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.recipes.all()
        if limit:
            queryset = queryset[:int(limit)]
        return SimpleRecipeSerializer(queryset, many=True).data
