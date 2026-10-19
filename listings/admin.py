from django.contrib import admin
from .models import Listing, ListingImage


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "price", "category", "is_sold", "created_at")
    list_filter = ("category", "is_sold")
    search_fields = ("title", "description")
    inlines = [ListingImageInline]