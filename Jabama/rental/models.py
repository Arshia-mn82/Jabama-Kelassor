from django.db import models
from django.contrib.auth.models import User


class Villa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    villa_type = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Booking(models.Model):
    villa = models.ForeignKey(Villa, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_people = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.villa.name} ({self.start_date} to {self.end_date})"

    def save(self, *args, **kwargs):

        if self.number_of_people > self.villa.capacity:
            raise ValueError("Number of people exceeds villa capacity")

        overlapping_bookings = Booking.objects.filter(
            villa=self.villa, start_date__lt=self.end_date, end_date__gt=self.start_date
        ).exclude(id=self.id)
        if overlapping_bookings.exists():
            raise ValueError("Villa is already booked for these dates")

        super().save(*args, **kwargs)
