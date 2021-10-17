from django.db import models
from users.models import User
from recipes.models.recipe import Recipe


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='fav_user',
        on_delete=models.CASCADE,
    )

    recipe = models.ForeignKey(
        Recipe,
        related_name='fav_recipe',
        on_delete=models.CASCADE,
    )