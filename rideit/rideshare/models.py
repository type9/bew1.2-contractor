from django.contrib.gis.db import models
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point, MultiPoint
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from accounts.models import UserProfile

class CommunityArea(models.Model):
    # TODO: Create a field that defines the geometric shape that a community operates in
    pass

class RideTrip(models.Model):
    start = models.PointField(blank = True, null=True, srid=4326)
    # TODO: make a "stops" feature which allow for on the way stops
    end = models.PointField(blank = True, null=True, srid=4326)

class Rider(User):
    class Meta:
        """Meta Class"""

        proxy = True

    def get_communities(self, user_rider):
        communities = [u.community for u in UserToCommunity.objects.filter(user=user_rider)]
        return communities

    def get_nonmember_communities(self, user_rider):
        members = Community.objects.values_list('members', flat='True')

        return communities

class Review(models.Model):
    reviewer = models.ForeignKey(
        Rider,
        null=True,
        related_name='driver_of_%(app_label)s_%(class)s',
        on_delete=models.PROTECT,
        help_text='The Rider who is offering to drive the trip'
    )   # TODO: Ask dani what CASCADE means on delete

    review = models.TextField(
        null=True,
        blank=True,
        help_text="user review string",
    )

    rating = models.IntegerField(
        null=True,
        blank=True,
    )

class RideShare(models.Model):
    trip = models.OneToOneField(
        RideTrip,
        on_delete=models.CASCADE,
        related_name='Ridetrip_of_%(app_label)s_%(class)s',
    )

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

    driver_user_profile = models.ForeignKey(
        UserProfile,
        null=True,
        related_name='userProfile_of_%(app_label)s_%(class)s',
        on_delete=models.PROTECT,
        help_text='The UserProfile of Rider who is offering to drive the trip'
    )

    driver = models.ForeignKey(
        Rider,
        related_name='driver_of_%(app_label)s_%(class)s',
        on_delete=models.PROTECT,
        help_text='The Rider who is offering to drive the trip'
    )   # TODO: Ask dani what CASCADE means on delete

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

    reviews = models.ManyToManyField(
        Review,
        blank=True,
        null=True,
        related_name='review_of_%(app_label)s_%(class)s',
        help_text='review object from rider'
    )

    @property
    def get_start(self):
        '''reverse geocodes start location. returns address'''
        long = self.trip.start.y
        lat = self.trip.start.x

        geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key={settings.GOOGLE_MAPS_API_KEY}'
        print(geocode_url)
        r = requests.get(geocode_url)
        print(f'REPSONSE: {r}')
        return r.json()['results'][0]['formatted_address']

    @property
    def get_end(self):
        '''reverse geocodes start location. returns address'''
        long = self.trip.end.y
        lat = self.trip.end.x

        geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key={settings.GOOGLE_MAPS_API_KEY}'
        r = requests.get(geocode_url)
        return r.json()['results'][0]['formatted_address']

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

    # areas = models.ManyToManyField(
    #     Location,
    #     blank=True,
    #     help_text='The areas in which this community will offer rideshares in (this is used for Riders to find the right communities)'
    # )

    rideshares = models.ManyToManyField(
        RideShare,
        blank=True,
        help_text='The current rideshares that are listed under this community'
    )
    blacklist = models.ManyToManyField(
        Rider,
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

    member_requests = models.ManyToManyField(
        Rider,
        symmetrical=False,
        related_name='request_members_of_%(app_label)s_%(class)s',
        blank=True,
        help_text='Requests from riders to join a community',
    )

    def __str__(self):
        return self.title

    # def get_members(self, member_username):
    #     return self.

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

    # @property
    # def get_members(self, input_community):
    #     members = UserToCommunity.objects.filter(community=input_community)
    #     return members

    def is_member(self, user_rider):
        if Rider.objects.get(username=user_rider.username) in self.members.get_queryset():
            return True
        else:
            return False

    @property
    def get_members(self):
        members = UserToCommunity.objects.filter(community=self)
        return members

class UserToCommunity(models.Model):
    """Relationship between rider and community"""

    user = models.ForeignKey(User, related_name="rider", default=1, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, related_name="community", default=1, on_delete=models.CASCADE)
