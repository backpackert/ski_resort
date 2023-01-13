from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import RegistrationAPIView, LoginAPIView

urlpatterns = [
    # path('login/', views.login, name='login'),
    #path('register/', views.register, name='register'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login')


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#
# path('register/', RegistrationAPIView.as_view(), name='register')