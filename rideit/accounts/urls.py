from django.urls import path
from accounts.views import SignUpView


urlpatterns = [
    path('account/signup/', SignUpView.as_view(), name='signup'),
]