import re

def calculate_imc_from_message(message):
    """
    Extrait poids et taille d'un message texte pour calculer l'IMC.
    Retourne un message formaté avec conseils selon l'IMC.
    """
    message = message.lower()
    matches = re.findall(r"(?:(poids|masse|kg|kilos|taille|hauteur|cm|m)[^\d]{0,10})?(\d+(?:[.,]\d+)?)", message)

    poids = None
    taille = None

    for keyword, number in matches:
        value = float(number.replace(",", "."))

        if any(kw in keyword for kw in ["poids", "kg", "kilos", "masse"]):
            poids = value
        elif any(kw in keyword for kw in ["taille", "hauteur", "cm"]):
            taille = value / 100 if value > 10 else value
        elif "m" in keyword:
            taille = value

    # Si les unités ne sont pas précisées
    if len(matches) == 2 and (not poids or not taille):
        n1 = float(matches[0][1].replace(",", "."))
        n2 = float(matches[1][1].replace(",", "."))

        if n1 > 30 and n2 < 3:
            poids, taille = n1, n2
        elif n2 > 30 and n1 < 3:
            poids, taille = n2, n1
        elif n1 > 100 and n2 > 30:  # ex: 175cm et 80kg
            poids = n2 if n2 < 250 else n1
            taille = (n1 if n1 < 250 else n2) / 100
        else:
            poids, taille = max(n1, n2), min(n1, n2)

    if poids and taille:
        imc = round(poids / (taille ** 2), 2)
        return f"📊 Votre IMC est **{imc}** (Poids: {poids}kg, Taille: {taille}m).\n\n{interpret_imc(imc)}"

    return "❌ Impossible de calculer votre IMC. Donnez un poids et une taille valides."

def interpret_imc(imc):
    """
    Fournit une interprétation de l'IMC avec conseils personnalisés.
    """
    if imc < 16.5:
        return "⚠️ Vous êtes en **dénutrition**. Il est important de consulter un professionnel de santé."
    elif imc < 18.5:
        return "ℹ️ Vous êtes en **maigreur**. Essayez d’atteindre un poids plus stable si possible."
    elif imc < 25:
        return "✅ Votre IMC est **normal**. Continuez à avoir une bonne hygiène de vie !"
    elif imc < 30:
        return "⚠️ Vous êtes en **surpoids**. Un peu d’activité physique régulière peut aider."
    elif imc < 35:
        return "⚠️ Vous êtes en **obésité modérée**. Une prise en charge médicale est conseillée."
    elif imc < 40:
        return "⚠️ Vous êtes en **obésité sévère**. Il est recommandé de consulter un professionnel."
    else:
        return "🚨 Vous êtes en **obésité morbide**. Une prise en charge urgente est fortement conseillée."
