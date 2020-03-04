from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from rideshare.models import Rider, RideShare, Community, RideTrip
from api.serializers import RiderSerializer, RideShareSerializer, CommunitySerializer, RideTripSerializer

# For Riders
class RiderList(ListCreateAPIView):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer

class RiderDetail(RetrieveDestroyAPIView):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer

# For Riders
class RideList(ListCreateAPIView):
    queryset = RideTrip.objects.all()
    serializer_class = RiderSerializer

class RideDetail(RetrieveDestroyAPIView):
    queryset = RideTrip.objects.all()
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
