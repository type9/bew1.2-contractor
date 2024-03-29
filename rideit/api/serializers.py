from rest_framework.serializers import ModelSerializer

from rideshare.models import Rider, RideShare, Community, RideTrip

class RiderSerializer(ModelSerializer):
    class Meta:
        model = Rider
        fields = '__all__'

class RideShareSerializer(ModelSerializer):
    class Meta:
        model = RideShare
        fields = '__all__'

class CommunitySerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class RideTripSerializer(ModelSerializer):
    class Meta:
        model = RideTrip
        fields = '__all__'
