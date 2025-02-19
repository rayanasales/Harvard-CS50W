from django.contrib import admin
from .models import User, AuctionListing, Bid, Comment, Watchlist
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'starting_bid', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username')
class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('listing__title', 'user__username', 'amount')
class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('listing__title', 'user__username', 'content')
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'listing__title')

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)