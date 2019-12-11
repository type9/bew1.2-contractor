from django.urls import path
from accounts.views import SignUpView


urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
]