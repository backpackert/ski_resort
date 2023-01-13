from django.contrib import admin

from .models import Parking, ParkingSpot, ParkingSpotInstance, SpotReservation


class ParkingAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')


class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('number', 'price', 'parking')
    search_fields = ('number', 'parking__name')
    list_select_related = ('parking', )


class ParkingSpotInstanceAdmin(admin.ModelAdmin):
    list_display = ('spot_id', 'parking_spot', 'status')
    search_fields = ('spot_id', 'status')


class SpotReservationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SpotReservation._meta.get_fields()]


admin.site.register(Parking, ParkingAdmin)
admin.site.register(ParkingSpot, ParkingSpotAdmin)
admin.site.register(ParkingSpotInstance, ParkingSpotInstanceAdmin)
admin.site.register(SpotReservation, SpotReservationAdmin)