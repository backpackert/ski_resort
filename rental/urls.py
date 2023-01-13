from django.urls import path, re_path
from .views import CategoriesEquipView, EquipItemsView, BasketView, AddProductIntoUserBasket,\
    DeleteProductFromUserBasket, CreateOrderView
from django_filters.views import FilterView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('equipment/', CategoriesEquipView.as_view(), name='rental'),
    path('equipment/<int:category_id>/', EquipItemsView.as_view(), name='equipment'),
    path('add-product/', AddProductIntoUserBasket.as_view(), name='add_to_basket'),
    path('get-user-basket/', BasketView.as_view(), name='basket'),
    path('delete-product/', DeleteProductFromUserBasket.as_view(), name='delete_product'),
    path('create-order/', CreateOrderView.as_view(), name='create_order')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
