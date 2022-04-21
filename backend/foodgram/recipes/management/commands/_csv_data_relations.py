from recipes.models import (Ingredient, Recipe,
                            AmountIngredientForRecipe, Tag,
                            Favorite, ShoppingCart)
from users.models import User

csv_data_relation = (
    {'model': Ingredient, 'filename': 'ingredients.csv'},
    {'model': Tag, 'filename': 'tags.csv'},
    {'model': User, 'filename': 'users.csv'},
    {'model': Recipe, 'filename': 'recipes.csv'},
    {'model': Recipe.tags.through, 'filename': 'recipes_tags.csv'},
    {'model': AmountIngredientForRecipe,
        'filename': 'amount_ingredient_for_recipe.csv'},
    {'model': Favorite, 'filename': 'favorites.csv'},
    {'model': ShoppingCart, 'filename': 'shopping_carts.csv'},
)
