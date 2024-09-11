from django.urls import path
from .views import *

urlpatterns = [
    path("villas/", VillaListCreateView.as_view(), name="villa-list-create"),
    path("villas/<int:pk>/", VillaDetailView.as_view(), name="villa-detail"),
    path("bookings/", BookingListCreateView.as_view(), name="booking-list-create"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("reviews/", ReviewListCreateView.as_view(), name="review-list-create"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
]
