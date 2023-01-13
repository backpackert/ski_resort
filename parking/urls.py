from django.urls import path
from .views import SpotReservationView, ParkingSpotInstanceListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('parking/reserve-spot/', SpotReservationView.as_view(), name='parking'),
    path('parking/', ParkingSpotInstanceListView.as_view(), name='whole_parking')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)