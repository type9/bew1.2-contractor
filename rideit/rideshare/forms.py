from django import forms
from rideshare.models import Community, RideShare
from django.contrib.gis.geos import Point

from location_field.forms.plain import PlainLocationField

class CommunityCreateForm(forms.ModelForm):
    """ Render and process a form based on the Page model. """
    class Meta:
        model = Community
        fields = ('title', 'description',)

# class RideShareCreateForm(forms.ModelForm):
#     """ Render a form for the Rideshare """
#     class Meta:
#         model = RideShare
#         fields = ('start_location', 'end_location', 'departure_date', 'cost_per_passenger')
#         widgets = {'ref': forms.HiddenInput(),}

class RideShareCreateForm(forms.Form):
    class Meta:
        widgets = {'ref': forms.HiddenInput(),}

    departure_date = forms.DateField()
    cost_per_passenger = forms.DecimalField(decimal_places=2, max_digits=5, help_text='Cost per passenger')