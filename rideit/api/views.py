from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from rideshare.models import Rider, RideShare, Community
from api.serializers import RiderSerializer, RideShareSerializer, CommunitySerializer

# For Riders
class RiderList(ListCreateAPIView):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer

class RiderDetail(RetrieveDestroyAPIView):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer

# For RiderShares
class RideShareList(ListCreateAPIView):
    queryset = RideShare.objects.all()
    serializer_class = RideShareSerializer

class RideShareDetail(RetrieveDestroyAPIView):
    queryset = RideShare.objects.all()
    serializer_class = RideShareSerializer

# For CommunitySerializer
class CommunityList(ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class CommunityDetail(RetrieveDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class CommunityBlacklist(RetrieveDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
