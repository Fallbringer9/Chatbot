from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Utilisateur supprimé}'} - {self.message[:50]}"

class FoodCache(models.Model):
    food_name = models.CharField(max_length=255, unique=True)
    calories = models.FloatField()
    protein = models.FloatField(null=True, blank=True)
    fat = models.FloatField(blank=True, null=True)
    carbohydrates = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_cached_food(food):
        """Vérifie si l'aliment est déja dans en cache  et mis à jour depuis 24H"""
        cached_food = FoodCache.objects.filter(food_name=food).first()
        if cached_food and cached_food.updated_at > now() - timedelta(days=1):
            return cached_food
        return None
