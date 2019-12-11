from django import forms
from rideshare.models import Community, RideShare, Location

from location_field.forms.plain import PlainLocationField


class CommunityCreateForm(forms.ModelForm):
    """ Render and process a form based on the Page model. """
    class Meta:
        model = Community
        fields = ('title', 'description',)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"

class RideShareCreateForm(forms.Form):
    """ Render a form for the Rideshare """
    departure_date = forms.DateField()
    cost_per_passenger = forms.DecimalField(decimal_places=2, max_digits=5, help_text='The cost the driver wishes to charge per passenger')