from django.db import models
from django.contrib.auth.models import User


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("books", "Books and notes"),
        ("electronics", "Electronics"),
        ("clothes", "Clothes and accessories"),
        ("room", "Room essentials"),
        ("stationery", "Stationery"),
        ("other", "Other"),
    ]
    CONDITION_CHOICES = [
        ("new", "New"),
        ("like_new", "Like new"),
        ("used", "Used"),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="listings/")

    def __str__(self):
        return f"Image for {self.listing.title}"