from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Villa, Booking
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def welcome(request):
    return JsonResponse("Welcome to Jabama", safe=False)


# Villa Views
class VillaListCreateView(ListCreateAPIView):
    queryset = Villa.objects.all()
    serializer_class = VillaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Villa.objects.filter(user = self.request.user)


class VillaDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Villa.objects.all()
    serializer_class = VillaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Villa.objects.filter(user = self.request.user)



# Booking Views
class BookingListCreateView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user = self.request.user)


class BookingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user = self.request.user)


class Login(TokenObtainPairView):
    pass


class Refresh(TokenRefreshView):
    pass
