import os
import random
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from django.core.cache import cache

load_dotenv()
EXERCISE_API_KEY = os.getenv("EXERCISE_API_KEY")

MUSCLE_MAP = {
    "pectoraux": "chest",
    "abdominaux": "abdominals",
    "biceps": "biceps",
    "mollets": "calves",
    "avant-bras": "forearms",
    "fessiers": "glutes",
    "ischio-jambiers": "hamstrings",
    "dos": "lats",
    "bas du dos": "lower_back",
    "milieu du dos": "middle_back",
    "cou": "neck",
    "quadriceps": "quadriceps",
    "trapèzes": "traps",
    "triceps": "triceps"
}

def get_exercise_info(muscle):
    """
    Reçoit un nom de muscle (ex: 'triceps'), traduit et appelle l’API pour proposer un exercice.
    """
    cache_key = f"exercise_{muscle.lower()}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    # 🧠 Traduire pour la requête API (si pas déjà en anglais)
    muscle_api = MUSCLE_MAP.get(muscle.lower(), GoogleTranslator(source="fr", target="en").translate(muscle).lower())

    url = f"https://api.api-ninjas.com/v1/exercises?muscle={muscle_api}"
    headers = {"X-Api-Key": EXERCISE_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        exercises = response.json()
        if exercises:
            exercise = random.choice(exercises)
            name = GoogleTranslator(source="en", target="fr").translate(exercise.get("name", "Exercice inconnu"))
            instructions = GoogleTranslator(source="en", target="fr").translate(exercise.get("instructions", ""))

            instructions = instructions.replace(" . ", ". ").replace(" , ", ", ").replace("  ", " ")

            response_text = f"💪 **{name}**\n\n📌 {instructions}"
            cache.set(cache_key, response_text, timeout=86400)
            return response_text

    return "❌ Aucun exercice trouvé pour ce muscle. Essayez un autre nom (ex: 'cuisses' au lieu de 'quadriceps')."
