from django.urls import path
from rideshare.views import CommunityListView, CommunityDetailView, CommunityCreateView, RideShareDetailView, RideShareCreateView, BlacklistView, BlockUser


urlpatterns = [
    path('', CommunityListView.as_view(), name='community-list-page'),
    path('cm/<str:slug>/', CommunityDetailView.as_view(), name='community-details-page'),
    path('createcommunity/', CommunityCreateView.as_view(), name='community-create-page'),

    path('rs/<int:pk>', RideShareDetailView.as_view(), name='rideshare-details-page'),
    path('cm/<str:slug>/newrs', RideShareCreateView.as_view(), name='rideshare-create-page'),

    # blacklist message route
    path('cm/blacklist/<str:slug>', BlacklistView.as_view(), name='blacklist-page'),

    # add blocked user to blacklist
    path('cm/blacklist/<str:slug>/<int:pk>', BlockUser, name='blacklist-page'),

]
