from recipes.models import AmountIngredientForRecipe, Ingredient, Recipe, Tag
from users.models import User

csv_data_relation = (
    {'model': Ingredient, 'filename': 'ingredients.csv'},
    {'model': Tag, 'filename': 'tags.csv'},
    {'model': User, 'filename': 'users.csv'},
    {'model': Recipe, 'filename': 'recipes.csv'},
    {'model': Recipe.tags.through, 'filename': 'recipes_tags.csv'},
    {'model': AmountIngredientForRecipe,
        'filename': 'amount_ingredient_for_recipe.csv'},
)
