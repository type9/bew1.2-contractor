from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy

from rideshare.models import Rider, RideShare, Community
from rideshare.forms import CommunityCreateForm, RideShareCreateForm


# Create your views here.
class CommunityListView(ListView):
    ''' Index page for communities'''
    model = Community

    def open_communities(self, request, communities):
        ''' set boolian for blacklist t/f '''
        # get current user
        current_user = request.user
        # stores all accessable communities
        new_communities = []

        # stores all blacklisted users
        blacklisted_users = []



        for community in communities:
            print(community)
            # check if current user is blacklisted
            print(community.blacklist.all())
            print("_____-")
                # print("blacklisted: " + blacklisted_user)
            for blacklisted_user in community.blacklist.all():
                print("_________________-")
                blacklisted_users.append(blacklisted_user)

                print(blacklisted_user)

            if current_user not in blacklisted_users:
                new_communities.append(community)


        return new_communities


    def get(self, request):
        '''GET a list of communities'''
        communities = self.open_communities(request, self.get_queryset().all())

        return render(request, 'community-list.html', {
            'communities': communities,
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
        }
        return render(request, 'rideshare-create.html', context)

    def post(self, request, *args, **kwargs):
        form = RideShareCreateForm(request.POST)
        community_slug = request.POST.get('slug', None)
        community = Community.objects.get(slug=community_slug)

        if form.is_valid() and community is not None:
            rideshare = form.save(commit=False)
            rideshare.driver = Rider.objects.get(id=request.user.id)
            rideshare.save()

            community.rideshares.add(rideshare)
            return HttpResponseRedirect(reverse('rideshare-details-page', args=[rideshare.id]))
        return render(request, 'rideshare-create.html', {'form': form})
