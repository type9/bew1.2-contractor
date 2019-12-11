from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy

from rideshare.models import Rider, RideShare, Community, Place
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

    def get(self, request, rideshare_id):
        rideshare = get_object_or_404(RideShare, pk=rideshare_id)
        return render(request, 'rideshare-details.html', {
            'rideshare': rideshare,
        })

class RideShareCreateView(CreateView):
    model = RideShare
    def get(self, request, *args, **kwargs):
        context = {'rideshare_details': RideShareCreateForm()}
        return render(request, 'rideshare-create.html', context)

    def post(self, request, slug, *args, **kwargs):
        community = self.get_queryset().get(slug__iexact=slug)
        form = RideShareCreateForm(request.POST)
        if form.is_valid():
            rideshare = form.save(commit=False)
            rideshare.driver = Rider.objects.get(id=request.user.id)
            rideshare.save()
            community.rideshares.add(rideshare)
            return HttpResponseRedirect(reverse('rideshare-details-page', args=[rideshare.id]))
        return render(request, 'rideshare-create.html', {'form': form})