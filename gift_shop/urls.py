from django.urls import path, re_path
from .views import CategoriesView, ProductItemsView
from django_filters.views import FilterView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='gift_shop'),
    path('categories/<int:category_id>/', ProductItemsView.as_view(), name='product'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('categories/(<int:category_id>/', ProductItemsView.as_view(), name='product')
# re_path('^categories/(?P<category_id>.+)/$', ProductItemsView.as_view(), name='product')