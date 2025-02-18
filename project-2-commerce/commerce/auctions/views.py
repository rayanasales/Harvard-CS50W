from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import AuctionListingForm
from .models import User, AuctionListing, Watchlist, Bid

def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('index')  # Redirect to a page after successful creation
    else:
        form = AuctionListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})

def listing_details(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    is_in_watchlist = False
    winning_bid = listing.bids.aggregate(Max('amount'))['amount__max']
    highest_bid = listing.bids.filter(amount=winning_bid).first() if winning_bid else None

    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()

        # Handle closing the auction
        if 'close_auction' in request.POST:
            if request.user == listing.user and listing.is_active:
                listing.is_active = False
                listing.winner = highest_bid.user if highest_bid else None
                listing.save()
                return redirect('listing_details', listing_id=listing_id)

    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "is_in_watchlist": is_in_watchlist,
        "bids": listing.bids.all().order_by('-created_at'),
        "highest_bid": highest_bid,
        "winner_message": "Congratulations! You have won this auction." if listing.winner == request.user else "",
        "loser_message": f"The auction has been won by {listing.winner.username}." if listing.winner and listing.winner != request.user else ""
    })

@login_required
def toggle_watchlist(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        watchlist_item.delete()
    return HttpResponseRedirect(reverse("listing_details", args=(listing_id,)))

@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    listings = [item.listing for item in watchlist_items]
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        listing = AuctionListing.objects.get(id=listing_id)
        bid_amount = Decimal(request.POST.get('bid_amount'))
        
        # Check if the bid is higher than the current and starting bid
        if bid_amount >= listing.starting_bid and (not listing.bids.exists() or bid_amount > listing.bids.latest('created_at').amount):
            new_bid = Bid(listing=listing, user=request.user, amount=bid_amount)
            new_bid.save()
            return redirect('listing_details', listing_id=listing_id)
        else:
            return render(request, "auctions/listing_details.html", {
                "listing": listing,
                "error_message": "Your bid must be higher than the current highest bid.",
                "is_in_watchlist": Watchlist.objects.filter(user=request.user, listing=listing).exists()
            })
    else:
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))