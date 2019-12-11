from django.urls import path
from rideshare.views import CommunityListView, CommunityDetailView, CommunityCreateView, RideShareDetailView, RideShareCreateView


urlpatterns = [
    path('', CommunityListView.as_view(), name='community-list-page'),
    path('cm/<str:slug>/', CommunityDetailView.as_view(), name='community-details-page'),
    path('createcommunity/', CommunityCreateView.as_view(), name='community-create-page'),

    path('rs/<int:pk>', RideShareDetailView.as_view(), name='rideshare-details-page'),
    path('cm/<str:slug>/newrs', RideShareCreateView.as_view(), name='rideshare-create-page'),
]