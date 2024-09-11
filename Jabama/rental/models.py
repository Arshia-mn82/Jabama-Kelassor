from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime


class Villa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    extra_price_per_person_per_night = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    weekend_price_multiplier = models.DecimalField(
        max_digits=4, decimal_places=2, default=1.50
    )
    seasonal_price_multiplier = models.DecimalField(
        max_digits=4, decimal_places=2, default=1.20
    )
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    villa_type = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    villa = models.ForeignKey(Villa, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_people = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.username} - {self.villa.name} ({self.start_date} to {self.end_date})"

    def calculate_price(self):
        total_nights = (self.end_date - self.start_date).days
        base_price = 0
        for day in range(total_nights):
            date = self.start_date + timedelta(days=day)
            price_for_night = self.villa.price_per_night

            if date.weekday() in [5, 6]:
                price_for_night *= self.villa.weekend_price_multiplier

            if date.month in [6, 7, 8]:
                price_for_night *= self.villa.seasonal_price_multiplier

            base_price += price_for_night

        extra_people = max(self.number_of_people - self.villa.capacity, 0)
        extra_price = (
            extra_people * self.villa.extra_price_per_person_per_night * total_nights
        )
        total_price = base_price + extra_price

        if total_nights > 7:
            total_price *= 0.95

        return total_price

    def save(self, *args, **kwargs):
        if self.number_of_people > self.villa.capacity:
            raise ValueError("Number of people exceeds villa capacity")

        overlapping_bookings = Booking.objects.filter(
            villa=self.villa, start_date__lt=self.end_date, end_date__gt=self.start_date
        ).exclude(id=self.id)

        if overlapping_bookings.exists():
            raise ValueError("Villa is already booked for these dates.")

        overlapping_user_bookings = Booking.objects.filter(
            user=self.user, start_date__lt=self.end_date, end_date__gt=self.start_date
        ).exclude(id=self.id)

        if overlapping_user_bookings.exists():
            raise ValueError("You have already booked a villa for these dates.")

        super().save(*args, **kwargs)

    def cancel(self):
        if self.start_date - datetime.now().date() > timedelta(days=1):
            self.status = "cancelled"
            self.save()
        else:
            raise ValueError(
                "Cancellation is not allowed within 24 hours of the start date."
            )


class Review(models.Model):
    villa = models.ForeignKey(Villa, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} review for {self.villa.name}"
