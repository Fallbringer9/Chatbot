from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from bot.services.brain import generate_response


from django.contrib.auth.mixins import LoginRequiredMixin



def home_view(request):
    return render(request,"chatbot/home.html")



class ChatbotView(LoginRequiredMixin, View):
    def get(self, request):
        """Affiche la page du chatbot"""
        return render(request, "bot/chat.html", {"username": request.user.username})

    def post(self, request):
        """Gère l'interaction avec le bot via HTMX"""
        user_message = request.POST.get("message", "").strip().lower()
        bot_response = generate_response(user_message)

        # ✅ Retourne une réponse HTML plutôt que du JSON

        return HttpResponse(f'<div class="message bot">{bot_response}</div>')


class RegisterView(View):
    def get(self, request):
        return render(request, "bot/register.html")  # Page d'inscription

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("chat")  # Redirige vers le chatbot après inscription

class LoginView(View):
    def get(self, request):
        return render(request, "bot/login.html")  # Page de connexion

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("chat")
        else:
            messages.error(request, "Identifiants incorrects.")
            return redirect("login")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")
