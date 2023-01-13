from django.urls import path, re_path
from . import views
from .views import ReviewListView, ReviewCreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name='review'),
    path('reviews/create/', ReviewCreateView.as_view(), name='create')


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)