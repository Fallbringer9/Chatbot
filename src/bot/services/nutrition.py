import os
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from django.core.cache import cache
from bot.models import FoodCache

load_dotenv()
NUTRITION_API_ID = os.getenv("NUTRITION_API_ID")
NUTRITION_API_KEY = os.getenv("NUTRITION_API_KEY")


def get_food_info(food):
    """
    Récupère les infos nutritionnelles d'un aliment donné (ex: 'pomme'),
    en le traduisant en anglais pour l’API Nutritionix.
    Résultat mis en cache + base de données pour performances.
    """
    cache_key = f"food_{food.lower()}"

    # 🔁 Vérifie le cache Redis
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    # 🗄️ Vérifie la base de données
    cached_food = FoodCache.get_cached_food(food)
    if cached_food:
        response_text = f"{cached_food.food_name} contient {cached_food.calories} kcal, {cached_food.protein}g de protéines."
        cache.set(cache_key, response_text, timeout=86400)
        return response_text

    # 🌍 Traduire en anglais
    translated_food = GoogleTranslator(source="fr", target="en").translate(food)

    # 🔗 Requête à l’API
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITION_API_ID,
        "x-app-key": NUTRITION_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json={"query": translated_food})

    if response.status_code == 200:
        food_data = response.json().get("foods", [])
        if not food_data:
            return "Je n’ai pas trouvé d'informations sur cet aliment."

        food_data = food_data[0]

        # 💾 Stockage
        cached_food, _ = FoodCache.objects.update_or_create(
            food_name=food.lower(),
            defaults={
                "calories": food_data['nf_calories'],
                "protein": food_data.get("nf_protein", 0),
                "fat": food_data.get("nf_total_fat", 0),
                "carbohydrates": food_data.get("nf_total_carbohydrate", 0)
            }
        )

        response_text = f"{food} contient {cached_food.calories} kcal, {cached_food.protein}g de protéines."
        cache.set(cache_key, response_text, timeout=86400)

        return response_text

    return "Erreur lors de la récupération des données nutritionnelles."

