from django.urls import path
from accounts.views import SignUpView

from .views import WelcomeView


app_name = "accounts"

urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('welcome', WelcomeView.as_view(), name='welcome-page')
]
