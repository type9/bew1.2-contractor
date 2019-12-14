# bew1.2-contractor
Final project for BEW 1.2. See /proposal.md

LIVE HERE: https://rideit.herokuapp.com/

The concept of this project is to create a 'subredditable' ridesharing platform. To achieve that I have seperate the database in three main structures

1) Rider (or user)
2) Community (collection of users and rideshares)
3) Rideshare (small collection of users with detail)

Using Django Auth, a user can login.
From this point they can create a community, or click on the currently existing communities to view their current rideshare offers.

Once inside a community they can create a rideshare for that community. This allows them to choose a start point, a departure date, and a cost per passenger. The website will automatically assign them as a driver.

Communities currently have no moderation rules yet but the models are in place to create the functionality.

Rideshare are geocoded from their lat/long coordinates 

This website is a proof of concept and is to be finished.

TODO:
- Fix map in rideshare form so a second point can be selected for the rideshare
- Add moderation tools for both communities and rideshares
- Make signup require contact details which become the body of a RideShare details page
- Add custom styling.