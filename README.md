# Chatbot Django

Ce projet est un chatbot web simple développé avec Django, conçu pour répondre à des questions basiques sur :

- le calcul de l'IMC
- les calories de certains aliments
- des exercices associés à un groupe musculaire

---

## Fonctionnalités

- Reconnaissance d’intentions de base (IMC, calories, exercices)
- Interface utilisateur avec HTMX (chat en direct)
- Calcul dynamique de l’IMC à partir de phrases comme "je pèse 70 kg pour 1m75"
- Structure modulaire (`brain.py`, `intents.py`, `imc.py`, etc.)

---

## Technologies

- Python 3.13
- Django
- HTMX
- HTML / CSS
- Regex (pour l'analyse des messages)
- Architecture MVC

---

## Structure du projet

