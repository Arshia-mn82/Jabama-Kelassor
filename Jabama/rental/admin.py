from django.contrib.admin import register, ModelAdmin
from .models import Villa, Booking


@register(Villa)
class VillaAdmin(ModelAdmin):
    list_display = ("name", "city", "price_per_night", "capacity", "villa_type")
    search_fields = ("name", "city", "villa_type")


@register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ("villa", "user", "start_date", "end_date", "number_of_people")
    list_filter = ("start_date", "end_date", "villa")
    search_fields = ("villa__name", "user__username")
