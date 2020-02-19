from django import forms
from rideshare.models import Community, RideShare, Location


class CommunityCreateForm(forms.ModelForm):
    """ Render and process a form based on the Page model. """
    class Meta:
        model = Community
        fields = ('title', 'description',)

class RideShareCreateForm(forms.ModelForm):
    """ Render a form for the Rideshare """
    class Meta:
        model = RideShare
        fields = ('start_location', 'end_location', 'departure_date',
                  'cost_per_passenger')
        widgets = {'ref': forms.HiddenInput(), }

# class RateAndReviewCreateForm(forms.ModelForm):
#     class Meta:
#         model = RideShare
#         fields = ('driver', 'passengers','start_location','end_location',
#                   'departure_date', 'rating', 'review')
