from django.urls import path
from rideshare.views import CommunityListView, CommunityDetailView, CommunityCreateView
from rideshare.views import RideShareDetailView, RideShareCreateView, BlacklistView
from rideshare.views import BlockUser, JoinCommunity, AcceptMemberRequest, RemoveRideShare, RateAndReviewRide

'''
Abbreviation Key:
    cm is community
    rs is rideshare
                        '''

urlpatterns = [
    # community list route
    path('', CommunityListView.as_view(), name='community-list-page'),
    # community detail route
    path('cm/<str:slug>/', CommunityDetailView.as_view(), name='community-details-page'),
    # community create route
    path('createcommunity/', CommunityCreateView.as_view(), name='community-create-page'),
    # Ride share detail route
    path('rs/<int:pk>', RideShareDetailView.as_view(), name='rideshare-details-page'),
    # create ride share route
    path('cm/<str:slug>/newrs', RideShareCreateView.as_view(),name='rideshare-create-page'),
    # blacklist message route slug=community slug
    path('cm/blacklist/<str:slug>', BlacklistView.as_view(), name='blacklist-page'),
    # add blocked user to blacklist slug=community slug, pk=user id
    path('cm/blacklist/<str:slug>/<int:pk>', BlockUser, name='blacklis-user-page'),
    # request to join private community by current user slug=community slug
    path('cm/join/<str:slug>', JoinCommunity, name='join-community-page'),
    # request to join private community by moderator pk=user id
    path('cm/join/<int:pk>/<str:slug>', JoinCommunity, name='join-community-page'),
    # reqeust to accept member to private community pk=user id
    path('cm/accept/<int:pk>/<str:slug>', AcceptMemberRequest, name='accept-member-page'),
    # request to remove a rideshare by moderator or owner
    path('cm/<str:slug>/remove/rs/<int:pk>', RemoveRideShare, name='remove-rideshare-page'),
    # request to review a RideShare
    path('cm/<str:slug>/rs/<int:rideshare_id>/review/<int:rating>', RateAndReviewRide, name='remove-rideshare-page'),
]
