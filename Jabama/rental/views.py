from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Villa, Booking, Review
from .serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def welcome(request):
    return JsonResponse("Welcome to Jabama", safe=False)


class VillaListCreateView(ListCreateAPIView):
    queryset = Villa.objects.all()
    serializer_class = VillaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["city", "price_per_night", "capacity"]
    ordering_fields = ["price_per_night", "capacity"]

    def get_queryset(self):
        return Villa.objects.filter(user=self.request.user)


class VillaDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Villa.objects.all()
    serializer_class = VillaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Villa.objects.filter(user=self.request.user)


class BookingListCreateView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class Login(TokenObtainPairView):
    pass


class Refresh(TokenRefreshView):
    pass


class ConfirmBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:

            booking = Booking.objects.get(pk=pk, user=request.user)

            if booking.status == "confirmed":
                return Response(
                    {"message": "Booking is already confirmed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            booking.status = "confirmed"
            booking.save()

            return Response(
                {
                    "message": "Booking confirmed successfully!",
                    "booking_id": booking.id,
                    "status": booking.status,
                },
                status=status.HTTP_200_OK,
            )

        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
            )
