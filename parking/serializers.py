from rest_framework import serializers
from .models import ParkingSpotInstance, RegisteredUser, SpotReservation, ParkingSpot
from django.contrib.auth import authenticate
from django.utils import timezone


class SpotReservationSerializer(serializers.ModelSerializer):
    def run_validation(self, data=None):
        return data

    class Meta:
        model = SpotReservation
        fields = '__all__'
        read_only_fields = ['id', ]

    def get_rental_days(self, data):
        rental_days = (data.end_rental_day - data.start_rental_day).days
        return rental_days

    def calculate_total_price(self, data):
        parking_spot_ids = data.get('chosen_spot')
        parking_spot = ParkingSpotInstance.objects.filter(id__in=parking_spot_ids).values('id', 'name', 'price')
        total_price = 0

        for spot in parking_spot:
            price = spot.get('price')
            rental_days = self.get_rental_days(data)
            total_price += price * rental_days

        user = self.context.get('request').user
        user.save()
        return total_price

    def get_total_number_of_spots(self, data):
        return len(data.get('chosen_spot'))

    def get_user(self):
        request = self.context.get('request')
        return request.user

    def create(self, validated_data):
        validated_data['total_price'] = self.calculate_total_price(validated_data)
        validated_data['total_number_of_spots'] = self.get_total_number_of_spots(validated_data)
        validated_data['total_rental_days'] = self.get_rental_days(validated_data)
        validated_data['user'] = self.get_user()
        return ParkingSpotInstance.objects.create(**validated_data)


class ParkingSpotInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingSpotInstance
        fields = '__all__'


# class ParkingSpotSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ParkingSpot
#         fields = '__all__'