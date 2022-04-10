from django.db import models

from users.models import User


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Чей список покупок'
    )
    recipe = models.ManyToManyField(
        "Recipe",
        related_name='shopping_carts',
        verbose_name='ID рецепта'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        ordering = ['id']

    def __str__(self) -> str:
        return ' / '.join(i.name for i in self.recipe.all())


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Чей список избранного'
    )
    recipe = models.ManyToManyField(
        "Recipe",
        related_name='favorites',
        verbose_name='ID рецепта'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ['id']

    def __str__(self) -> str:
        return ' / '.join(i.name for i in self.recipe.all())


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['id']

    # def __str__(self) -> str:
    #     return self.user.username + ' подписался на ' + self.author.username


class Recipe(models.Model):
    tags = models.ManyToManyField(
        "Tag",
        related_name='recipes',
        verbose_name='Тег'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        "Ingredient",
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='media/recipes/images/'
    )
    text = models.TextField(
        verbose_name='Текст рецепта'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['id']

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единца измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['id']

    def __str__(self) -> str:
        return self.name + ', ' + self.measurement_unit


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет в HEX',
        max_length=7,
        unique=True
    )
    slug = models.CharField(
        verbose_name='Cлаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']

    def __str__(self) -> str:
        return self.name
