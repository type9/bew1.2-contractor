import requests

from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

from mapbox_location_field.models import LocationField

class Location(models.Model):
    location = LocationField()

class Rider(User):
    class Meta:
        proxy = True




class RideShare(models.Model):
    start_location = LocationField()
    end_location = LocationField()

    return_trip = models.BooleanField(
        blank=True,
        null=True,
        help_text='If the driver is taking passengers on the ride back'
    )

    departure_date = models.DateField(
        help_text='When the driver plans to depart from starting location'
    )
    return_date = models.DateField(
        blank=True,
        null=True,
        help_text='OPTIONAL: When the driver plans to return from end location (if is offering return trip)'
    )

    driver = models.ForeignKey(
        Rider,
        related_name='driver_of_%(app_label)s_%(class)s',
        on_delete=models.PROTECT,
        help_text='The Rider who is offering to drive the trip'
    ) # TODO: Ask dani what CASCADE means on delete

    pending_passengers = models.ManyToManyField(
        Rider,
        blank=True,
        null=True,
        related_name='pendingpassenger_of_%(app_label)s_%(class)s',
        help_text='The passengers who whish to embark on this trip but have not been accepted by the driver yet'
    )
    passengers = models.ManyToManyField(
        Rider,
        blank=True,
        null=True,
        related_name='passenger_of_%(app_label)s_%(class)s',
        help_text='The passengers who will be embarking on this trip'
    )

    cost_per_passenger = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        help_text='The cost the driver wishes to charge per passenger')
        # TODO: Make cost configurable

    class Rate(models.IntegerChoices):
        one_star = 1
        two_stars = 2
        three_stars = 3
        four_stars = 4
        five_stars = 5

    rating = models.IntegerField(choices=Rate.choices)


    review = models.TextField(
        blank=True,
        help_text='drivers and riders can share reviews of the trip')

    @property
    def get_start(self):
        '''reverse geocodes start location. returns address'''
        long = float(self.start_location[0])
        lat = float(self.start_location[1])
        # geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key={settings.GOOGLE_API_KEY}'
        # r = requests.get(geocode_url)
        # print(f'REPSONSE: {r}')
        # return r.json()['results'][0]['formatted_address']
        return f'LONG:{long}, LAT:{lat}'

    @property
    def get_end(self):
        '''reverse geocodes start location. returns address'''
        long = float(self.end_location[0])
        lat = float(self.end_location[1])
        # geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key={settings.GOOGLE_API_KEY}'
        # r = requests.get(geocode_url)
        # return r.json()['results'][0]['formatted_address']
        return f'LONG:{long}, LAT:{lat}'


class Community(models.Model):
    title = models.CharField(max_length=settings.COMMUNITY_NAME_MAX_LEN, unique=True, help_text='Unique name for you rideshare community')
    blacklist_users = models.CharField(max_length=10000, blank=True, unique=False, help_text='Users in blacklist')

    slug = models.CharField(
        max_length=settings.COMMUNITY_NAME_MAX_LEN, blank=True, editable=False,
        help_text="Unique URL path to access this community. Generated by the system."
    )

    description = models.TextField(
        null=True,
        help_text="A description of your rideshare community"
    )

    owner = models.ForeignKey(
        Rider,
        related_name='owner_of_%(app_label)s_%(class)s',
        on_delete=models.PROTECT,
        help_text='The Rider that owns the community'
    )
    moderators = models.ManyToManyField(
        Rider,
        related_name='moderator_of_%(app_label)s_%(class)s',
        help_text='The Riders that manage the community. Designated by the owner.',
        blank=True
    )
    members = models.ManyToManyField(
        Rider,
        related_name='member_of_%(app_label)s_%(class)s',
        blank=True,
        help_text='The Riders that are allowed to create and participate in ridesharing in this community',
    )

    areas = models.ManyToManyField(
        Location,
        blank=True,
        help_text='The areas in which this community will offer rideshares in (this is used for Riders to find the right communities)'
    )

    rideshares = models.ManyToManyField(
        RideShare,
        blank=True,
        help_text='The current rideshares that are listed under this community'
    )
    blacklist = models.ManyToManyField(Rider,
        symmetrical=False,
        related_name='BL_members_of_%(app_label)s_%(class)s',
        blank=True,
        help_text='The Riders that are allowed to create and participate in ridesharing in this community',
    )

    # community private bool
    private = models.BooleanField(
        blank=True,
        null=True,
    )

    member_requests = models.ManyToManyField(Rider,
        symmetrical=False,
        related_name='request_members_of_%(app_label)s_%(class)s',
        blank=True,
        help_text='Requests from riders to join a community',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ Returns a fully-qualified path for a page (/my-community). """
        path_components = {'slug': self.slug}
        return reverse('community-details-page', kwargs=path_components)

    def save(self, *args, **kwargs):
        """ Creates a URL safe slug automatically when a new a page is created. """
        if not self.pk:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Community, self).save(*args, **kwargs)

    def get_rideshares(self):
        return self.rideshares
