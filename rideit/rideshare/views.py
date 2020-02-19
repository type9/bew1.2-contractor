from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from http.client import responses
from django.http import HttpResponse

from rideshare.models import Rider, RideShare, Community
from rideshare.forms import CommunityCreateForm, RideShareCreateForm


# Create your views here.
class CommunityListView(ListView):
    ''' Index page for communities'''
    model = Community



    def get(self, request):
        '''GET a list of communities'''
        communities = self.get_queryset().all()

        return render(request, 'community-list.html', {
            'communities': communities,
        })



class CommunityDetailView(DetailView):
    '''Community page'''
    model = Community

    def open_communities(self, request, community):
        ''' set boolian for blacklist t/f '''
        # get current user
        current_user = request.user
        # stores all blacklist users
        blacklisted_users = community.blacklist.all()
        # loop over blacklist users
        for blacklist_user in blacklisted_users:
            # check if current blacklist user is current user
            if blacklist_user == current_user:
                return True # blacklist user found return true


    def get(self, request, slug):
        community = self.get_queryset().get(slug__iexact=slug)

        banned = self.open_communities(request, community)

        if banned == True:
            print("User is blocked from community")
            return render(request, 'blacklist.html')

        else:
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


class BlacklistView(DetailView):


    def get(self, request):
        return render(request, 'blacklist.html')


# Add user to blocklist
def BlockUser(request, slug, pk):
    # user making request
    user = request.user

    # block user 
    block_user = get_object_or_404(Rider, pk=pk)

    # get community
    community = get_object_or_404(Community, slug=slug)
        # question = get_object_or_404(Question, pk=question_id)

    # get user to be added to blacklist 
    if user == community.owner or user in community.moderators.all():
        # community.blacklist += block_user
        print("{} user added to blacklist".format(block_user))
        community.blacklist.add(block_user)
        community.save()
        return render(request, 'blacklist.html', {'block': True, 'user': block_user})

    else: 
        return render(request, 'blacklist.html', {'block': False, 'user': block_user})

    

    