from django.urls import path

from api.views import RiderList, RiderDetail, RideShareList, RideShareDetail, CommunityList, CommunityDetail, CommunityBlacklist

urlpatterns = [
    path('riders/', RiderList.as_view(), name='riders'),
    path('riders/<int:pk>', RiderDetail.as_view(), name='rider_details'),

    path('rideshares/', RideShareList.as_view(), name='rideshares'),
    path('rideshares/<int:pk>', RideShareDetail.as_view(), name='rideshare_details'),

    path('communities/', CommunityList.as_view(), name='communities'),
    path('communities/<int:pk>', CommunityDetail.as_view(), name='community_details'),

    path('communities/<int:pk>/blacklist', CommunityBlacklist.as_view(), name='community_blacklist'),
]
