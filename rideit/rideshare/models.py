from django.db import models

from django.conf import settings
from django.contrib.auth.models import User

from location_field.models.plain import PlainLocationField # provides a location field
from phone_field import PhoneField # provides a phonefield

class Place(models.Model):
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7)

class Rider(User):
    class Meta:
        proxy = True

class RideShare(models.Model):
    start_location = models.ForeignKey(
        Place,
        related_name='startlocation_of_%(app_label)s_%(class)s',
        on_delete=models.CASCADE,
        help_text='The start location of this rideshare'
    ) # TODO: Ask dani what CASCADE means on delete
    end_location = models.ForeignKey(
        Place,
        related_name='endlocation_of_%(app_label)s_%(class)s',
        on_delete=models.CASCADE,
        help_text='The end location of this rideshare'
    )

    return_trip = models.BooleanField(help_text='If the driver is taking passengers on the ride back')

    departure_date = models.DateField(help_text='When the driver plans to depart from starting location')
    return_date = models.DateField(help_text='OPTIONAL: When the driver plans to return from end location (if is offering return trip)')

    driver = models.ForeignKey(
        Rider,
        related_name='driver_of_%(app_label)s_%(class)s',
        on_delete=models.PROTECT,
        help_text='The Rider who is offering to drive the trip'
    ) # TODO: Ask dani what CASCADE means on delete
    pending_passengers = models.ManyToManyField(
        Rider,
        related_name='pendingpassenger_of_%(app_label)s_%(class)s',
        help_text='The passengers who whish to embark on this trip but have not been accepted by the driver yet'
    )
    passengers = models.ManyToManyField(
        Rider,
        related_name='passenger_of_%(app_label)s_%(class)s',
        help_text='The passengers who will be embarking on this trip'
    )

    cost_per_passenger = models.DecimalField(decimal_places=2, max_digits=5, help_text='The cost the driver wishes to charge per passenger') # TODO: Make cost configurable

class Community(models.Model):
    name = models.CharField(max_length=settings.COMMUNITY_NAME_MAX_LEN, unique=True, help_text='Unique name for you rideshare community')

    owner = models.ForeignKey(Rider,
        related_name='owner_of_%(app_label)s_%(class)s',
        on_delete=models.PROTECT,
        help_text='The Rider that owns the community'
    )
    moderators = models.ManyToManyField(Rider,
        related_name='moderator_of_%(app_label)s_%(class)s',
        help_text='The Riders that manage the community. Designated by the owner.'
    )
    members = models.ManyToManyField(
        Rider,
        related_name='member_of_%(app_label)s_%(class)s',
        help_text='The Riders that are allowed to create and participate in ridesharing in this community',
    )
    areas = models.ManyToManyField(Place, help_text='The areas in which this community will offer rideshares in (this is used for Riders to find the right communities)')
    
    rideshares = models.ManyToManyField(RideShare, help_text='The current rideshares that are listed under this community')