from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy

from rideshare.models import Rider, RideShare, Community, RideTrip
from rideshare.forms import CommunityCreateForm, RideShareCreateForm


# Create your views here.
class CommunityListView(ListView):
    ''' Index page for communities'''
    model = Community

    def get(self, request):
        '''GET a list of communities'''
        communities = self.get_queryset().all()
        return render(request, 'community-list.html', {
            'communities': communities
        })

class CommunityDetailView(DetailView):
    '''Community page'''
    model = Community

    def get(self, request, slug):
        community = self.get_queryset().get(slug__iexact=slug)
        rideshares = community.get_rideshares().get_queryset()
        return render(request, 'community-details.html', {
            'community': community,
            'rideshares': rideshares
        })

class CommunityCreateView(CreateView):
    '''Community creation form'''
    model = Community
    
    def get(self, request, *args, **kwargs):
        context = {'form': CommunityCreateForm()}
        return render(request, 'community-create.html', context)

    def post(self, request, *args, **kwargs):
        form = CommunityCreateForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.owner = Rider.objects.get(id=request.user.id)
            community.save()
            return HttpResponseRedirect(reverse('community-details-page', args=[community.slug]))
        return render(request, 'community-create.html', {'form': form})

class RideShareDetailView(DetailView):
    '''Rideshare detail view'''
    model = RideShare

    def get(self, request, pk):
        rideshare = get_object_or_404(RideShare, pk=pk)
        start = rideshare.get_start
        end = rideshare.get_end
        return render(request, 'rideshare-details.html', {
            'rideshare': rideshare,
            'start': start,
            'end': end
        })

class RideShareCreateView(CreateView):
    model = RideShare
    def get(self, request, slug, *args, **kwargs):
        context = {
            'form': RideShareCreateForm(),
            'slug': slug,
            'key': settings.GOOGLE_MAPS_API_KEY,
            'default_lat': -25.344,
            'default_lng': 131.036,
        }
        return render(request, 'rideshare-create.html', context)

    def post(self, request, *args, **kwargs):
        form = RideShareCreateForm(request.POST)
        community_slug = request.POST.get('slug', None)
        community = Community.objects.get(slug=community_slug)

        if form.is_valid() and community is not None:
            new_rs = RideShare()
            new_trip = RideTrip()
            new_trip.start = form.cleaned_data['start_location']
            new_trip.end = form.cleaned_data['end_location']

            new_rs.trip = new_trip
            new_rs.driver = Rider.objects.get(id=request.user.id)
            new_rs.departure_date = form.cleaned_data['departure_date']
            new_rs.cost_per_passenger = form.cleaned_data['cost_per_passenger']

            new_rs.save()

            community.rideshares.add(new_rs)
            return HttpResponseRedirect(reverse('rideshare-details-page', args=[new_rs.id]))
        return render(request, 'rideshare-create.html', {'form': form})