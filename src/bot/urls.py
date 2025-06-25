from django.urls import path
from .views import ChatbotView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path('chat/',ChatbotView.as_view(), name='chat'),

# Authentification
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

]