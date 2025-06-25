import os
from dotenv import load_dotenv
from bot.services.nutrition import get_food_info
from bot.services.exercises import get_exercise_info




# Charger les variables d’environnement depuis .env
load_dotenv()

# Récupérer les clés API depuis .env
NUTRITION_API_ID = os.getenv("NUTRITION_API_ID")
NUTRITION_API_KEY = os.getenv("NUTRITION_API_KEY")
EXERCISE_API_KEY = os.getenv("EXERCISE_API_KEY")

# Vérification des clés API
if not NUTRITION_API_ID or not NUTRITION_API_KEY:
    raise ValueError("⚠️ Clé API Nutritionix manquante ! Vérifie ton fichier .env")
if not EXERCISE_API_KEY:
    raise ValueError("⚠️ Clé API Ninja Exercises manquante ! Vérifie ton fichier .env")


def get_bot_response(message):
    message = message.lower().strip()

    if "imc" in message:
        return "Pour calculer votre IMC, envoyez-moi votre poids et votre taille !"

    if "exercice" in message:
        muscle = message.replace("exercice", "").strip()
        return get_exercise_info(muscle)

    if "calories" in message:
        food = message.replace("calories", "").strip()
        return get_food_info(food)

    return "Je ne comprends pas encore cette question."





