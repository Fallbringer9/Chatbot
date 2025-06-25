INTENTS = {
    "get_food_info": ["calories", "kcal", "aliment", "nourriture", "manger", "bouffe"],
    "get_exercise_info": ["exercice", "muscle", "muscles", "biceps", "pectoraux", "abdos", "fessiers"],
    "calculate_imc": ["imc", "indice", "masse", "poids", "taille", "kg", "cm", "m"]
}




def detect_intent(message):
    message = message.lower()
    intent_scores = {}

    for intent, keywords in INTENTS.items():
        score = sum(1 for keyword in keywords if keyword in message)
        if score > 0:
            intent_scores[intent] = score

    if intent_scores:
        # Renvoie l'intent avec le plus de mots trouvés
        return max(intent_scores, key=intent_scores.get)

    return None





