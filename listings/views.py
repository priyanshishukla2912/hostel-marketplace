from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import ListingForm, ListingEditForm
from .models import Listing, ListingImage


def home(request):
    listings = []
    if request.user.is_authenticated:
        listings = Listing.objects.filter(is_sold=False).prefetch_related("images")
    return render(request, "home.html", {"listings": listings})


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            for img in form.cleaned_data["images"]:
                ListingImage.objects.create(listing=listing, image=img)
            return redirect("listing_detail", pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, "listings/listing_form.html", {"form": form})


@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "listings/listing_detail.html", {"listing": listing})


@login_required
def my_listings(request):
    listings = Listing.objects.filter(seller=request.user).prefetch_related("images")
    return render(request, "listings/my_listings.html", {"listings": listings})


@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == "POST":
        form = ListingEditForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            for img in form.cleaned_data["images"]:
                ListingImage.objects.create(listing=listing, image=img)
            return redirect("listing_detail", pk=listing.pk)
    else:
        form = ListingEditForm(instance=listing)
    return render(request, "listings/listing_edit.html", {"form": form, "listing": listing})


@login_required
@require_POST
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    listing.delete()
    return redirect("my_listings")


@login_required
@require_POST
def toggle_sold(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    listing.is_sold = not listing.is_sold
    listing.save()
    return redirect("my_listings")


@login_required
@require_POST
def delete_image(request, pk):
    image = get_object_or_404(ListingImage, pk=pk, listing__seller=request.user)
    listing = image.listing
    if listing.images.count() > 1:
        image.delete()
    return redirect("edit_listing", pk=listing.pk)