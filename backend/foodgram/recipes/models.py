from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.db.models import F, Q

from .validators import hex_validator

User = get_user_model()


class ShoppingCart(models.Model):
    """Модель 'Список покупок' пользователя.

    Validators:
        - Рецепты в списке покупок не могут повторяться. Т.е. пользователь,
        может добавить рецепт только один раз.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='чей список покупок'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='ID рецепта'
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_cart')
        ]


class Favorite(models.Model):
    """Модель 'Избранное' пользователя.

    Validators:
        - Рецепты в избранном не могут повторяться. Т.е. пользователь,
        может добавить рецепт только один раз.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='чей список избранного'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='ID рецепта'
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite')
        ]


class Subscription(models.Model):
    """Модель 'Подписки' пользователя.

    Validators:
        - Пользователь не может подписаться сам на себя.
        - Каждый пользователь может подписаться на другого пользователя только 
        один раз.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='автор'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'),
            models.CheckConstraint(
                check=~Q(user=F('author')), name='user_not_author')
        ]

    def __str__(self) -> str:
        return f'подписчик {self.user.username}, автор {self.author.username}'


class Recipe(models.Model):
    """Модель 'Рецепты' пользователя.

    Validators:
        - Поле cooking_time (Время приготовления) не может быть меньше 1.
    """
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='тег'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipes',
        verbose_name='ингредиент'
    )
    name = models.CharField(
        verbose_name='название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='картинка рецепта',
        upload_to='media/recipes/images/'
    )
    text = models.TextField(
        verbose_name='текст рецепта'
    )
    cooking_time = models.IntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное время приготовления 1 минута'),),
        verbose_name='время приготовления'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['id']

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Модель 'Ингредиенты' для рецепта.

    Validators:
        - Каждый ингредиент должен быть уникальным.
    """
    name = models.CharField(
        verbose_name='название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='единца измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_ingredient')
        ]

    def __str__(self) -> str:
        return self.name


class AmountIngredientForRecipe(models.Model):
    """Модель 'Количество ингредиента для рецепта'.

    Validators:
        - В одном рецепте каждый игредиент уникальный.
        - Поле amount (Количество ингредиента) не может быть меньше 1.
    """
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='amountingredientforrecipes',
        verbose_name='ID рецепта'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='amountingredientforrecipes',
        verbose_name='ID ингредиента'
    )
    amount = models.IntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное количество ингридиентов 1'),),
        verbose_name='количество ингредиента'
    )

    class Meta:
        verbose_name = 'количество ингредиента для рецепта'
        verbose_name_plural = 'количество ингредиента для рецепта'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient')
        ]

    def __str__(self) -> str:
        return (f'{self.recipe.name} | {self.ingredient.name} | '
                f'{str(self.amount)} | {self.ingredient.measurement_unit}')


class Tag(models.Model):
    """Модель 'Теги' для рецептов.

    Validators:
        - Каждый тег должен быть уникальным.
        - Поле color (Цвет в HEX) не пропускает некорректные HEX цвета.
    """
    name = models.CharField(
        verbose_name='название тега',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='цвет в HEX',
        max_length=7,
        unique=True,
        validators=([hex_validator])
    )
    slug = models.CharField(
        verbose_name='слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color', 'slug'],
                name='unique_recipe_tag')
        ]

    def __str__(self) -> str:
        return self.name
