from django.shortcuts import render
from rest_framework.views import APIView
from django.views import generic
from .models import ParkingSpotInstance, ParkingSpot
from rest_framework.permissions import IsAuthenticated
from .serializers import SpotReservationSerializer, ParkingSpotInstanceSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class SpotReservationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = SpotReservationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()

        return Response(serializer.data, status=200)


class ParkingSpotInstanceListView(generic.ListView):
    queryset = ParkingSpotInstance.objects.all()
    serializer_class = ParkingSpotInstanceSerializer


# class ParkingSpotListView(generic.ListView):
#     queryset = ParkingSpot.objects.all()
#     serializer_class = ParkingSpotSerializer