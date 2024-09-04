from django.contrib import admin
from django.urls import path,include
from rental.views import (
    VillaListCreateView,
    VillaDetailView,
    BookingListCreateView,
    BookingDetailView,
    welcome,
    Login,
    Refresh,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("welcome/", welcome),
    path("admin/", admin.site.urls),
    path("villa/", include("rental.urls")),
    path("token/", Login.as_view(), name="token_obtain_pair"),
    path("token/refresh/", Refresh.as_view(), name="token_refresh"),
]
