from bot.services.intents import detect_intent
from bot.services.imc import calculate_imc_from_message
from bot.services.exercises import get_exercise_info
from bot.services.nutrition import get_food_info


def generate_response(message):
    intent = detect_intent(message)

    if intent == "calculate_imc":
        return calculate_imc_from_message(message)
    elif intent == "get_food_info":
        return get_food_info(message)
    elif intent == "get_exercise_info":
        return get_exercise_info(message)

    return "❌ Je ne comprends pas encore cette question. Essaie par exemple 'calories pomme' ou 'exercice biceps'."

