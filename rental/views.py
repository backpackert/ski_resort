from django.views import generic
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import EquipCategory, EquipItem, Basket
from .serializers import EquipCategoriesSerializer, EquipItemsSerializer, BasketSerializer, \
    AddProductSerializer, DeleteProductSerializer, CreateOrderSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import F


class CategoriesEquipView(generic.ListView):
    queryset = EquipCategory.objects.all()
    serializer_class = EquipCategoriesSerializer(many=True)
    print(EquipCategory.objects.first().__dict__)


class EquipItemsView(generic.ListView):
    queryset = EquipItem.objects.all()
    serializer_class = EquipItemsSerializer(many=True)

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return EquipItem.objects.filter(category_id=category_id)


class AddProductIntoUserBasket(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.user.id
        print(f"user_id': {user_id}")
        product_id = request.data.get('product_id')
        print(f"Request data: {product_id}")

        input_serializer = AddProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product = get_object_or_404(EquipItem, id=input_serializer.data.get('product_id'))

        basket = Basket()
        basket.user = request.user
        basket.product = product
        basket.number_of_items = 1
        basket.number_of_days = 1
        basket.save()

        object, created = Basket.objects.get_or_create(user=request.user, product=product)
        if object.number_of_items:
            object.number_of_items += input_serializer.data.get('number_of_items')
        else:
            object.number_of_items = input_serializer.data.get('number_of_items')
        object.save()

        return Response(status=200)


class DeleteProductFromUserBasket(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        user = request.user
        serializer = DeleteProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_item = get_object_or_404(EquipItem, id=serializer.data.get('product_item_id'))
        Basket.objects.get(user=user, product=product_item).delete()

        return Response(status=200)


class BasketView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        basket = EquipItem.objects.prefetch_related('basket_set').filter(basket__user=user).\
            values("name", "price", number_of_items=F("basket__number_of_items"),
            number_of_days=F('basket__number_of_days'))
        print(f"Basket: {basket}")

        serializer = BasketSerializer({"products": basket})

        return Response(serializer.data, status=200)


class CreateOrderView(APIView):
    permission_classes = (IsAuthenticated,)

    # @swagger_auto_schema(
    #     request_body=CreateOrderSerializer,
    #     request_method='POST',
    #     responses={
    #         200: CreateOrderSerializer
    #     }
    # )
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(serializer.data, status=200)