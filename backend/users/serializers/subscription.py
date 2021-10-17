from djoser.serializers import UserSerializer
from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscription
from recipes.models import Recipe
from users.models import User, Subscription
from users.serializers.user import CustomUserSerializer


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',)
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'subscribed']
            )
        ]

    def validate(self, data):
        user = self.context.get('request').user
        subscribed = data.get('subscribed')
        if user == subscribed:
            raise serializers.ValidationError("Users can't subscribe to themselves.")
        return data

    def get_recipes_count(self, obj):
        # user = self.context.get('request').user
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        # user = self.context.get('request').user
        serializer = RecipeSubscriptionSerializer(
            Recipe.objects.filter(author=obj),
            many=True
        )
        return serializer.data

    # def to_representation(self, instance):
    #     return model_to_dict(instance)


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        model = Recipe