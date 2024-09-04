from rest_framework import serializers
from .models import Villa, Booking

class BookingDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class VillaSerializer(serializers.ModelSerializer):
    bookings = BookingDateSerializer(many=True, read_only=True)

    class Meta:
        model = Villa
        fields = '__all__'
