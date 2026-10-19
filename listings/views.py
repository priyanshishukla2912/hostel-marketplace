from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ListingForm
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