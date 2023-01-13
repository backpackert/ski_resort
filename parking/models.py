from django.db import models
from django.conf import settings
from rental.models import RegisteredUser
import uuid
from datetime import date
from django.utils import timezone

user = settings.AUTH_USER_MODEL


class Parking(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(default=100, blank=True, null=True)

    def __str__(self):  # метод строковой репрезентации в админке, чтобы красиво отображалось
        return self.name # будет возвращать только имя


class ParkingSpot(models.Model):
    number = models.IntegerField()
    price = models.DecimalField(default=10, max_digits=10, decimal_places=2)
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.number}'

    class Meta:
        verbose_name = 'Parking spot'
        verbose_name_plural = 'Parking spots'


class ParkingSpotInstance(models.Model):
    spot_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               help_text="Unique ID for this particular spot across whole parking")
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.SET_NULL, null=True)
    RESERVATION_STATUSES = (('a', 'Available'),
                            ('r', 'Reserved'))
    status = models.CharField(max_length=1, choices=RESERVATION_STATUSES, blank=True, default='a',
                              help_text='Spot availability')

    def __str__(self):
        return f'{self.parking_spot}'


class SpotReservation(models.Model):
    RESERVATION_STATUSES = (('Booked', 'Booked'),
                            ('Not confirmed', 'Not confirmed'))
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    chosen_spot = models.TextField(default=None, null=True)
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_number_of_spots = models.IntegerField()
    start_rental_day = models.DateField(default=date.today, null=True, blank=True)
    end_rental_day = models.DateField(default=date.today, null=True, blank=True)
    rental_days = models.IntegerField(blank=True, null=True)
    reservation_status = models.CharField(max_length=20, choices=RESERVATION_STATUSES, blank=True,
                                     help_text='Reservation status')

    class Meta:
        ordering = ["end_rental_day"]

    def __str__(self):
        return self.chosen_spot
