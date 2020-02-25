from django.contrib import admin
from .models import Location, Rider, RideShare, Community, UserToCommunity

# Register your models here.
admin.site.register(Location)
admin.site.register(Rider)
admin.site.register(RideShare)
admin.site.register(Community)
admin.site.register(UserToCommunity)
