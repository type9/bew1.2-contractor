from django import forms

from rideshare.models import Community, RideShare, Review
from django.contrib.gis.geos import Point

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
        model = RideShare
        fields = ('start_location', 'end_location', 'departure_date',
                  'cost_per_passenger')
        widgets = {'ref': forms.HiddenInput(), }

    departure_date = forms.DateField()
    cost_per_passenger = forms.DecimalField(decimal_places=2, max_digits=5, help_text='Cost per passenger')

    start_lat = forms.DecimalField(required=False, widget=forms.HiddenInput())
    start_long = forms.DecimalField(required=False, widget=forms.HiddenInput())
    end_lat = forms.DecimalField(required=False, widget=forms.HiddenInput())
    end_long = forms.DecimalField(required=False, widget=forms.HiddenInput())

class RateAndReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review', 'reviewer','rating')
