from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.create_listing, name="create_listing"),
    path("<int:pk>/", views.listing_detail, name="listing_detail"),
]