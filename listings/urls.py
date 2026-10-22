from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.create_listing, name="create_listing"),
    path("mine/", views.my_listings, name="my_listings"),
    path("<int:pk>/", views.listing_detail, name="listing_detail"),
    path("<int:pk>/edit/", views.edit_listing, name="edit_listing"),
    path("<int:pk>/delete/", views.delete_listing, name="delete_listing"),
    path("<int:pk>/sold/", views.toggle_sold, name="toggle_sold"),
    path("image/<int:pk>/delete/", views.delete_image, name="delete_image"),
]