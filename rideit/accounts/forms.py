from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    """Form for UserProfile."""

    class Meta:
        """Metadata about this form."""

        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'profile_pic', 'number')
