from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.urls import reverse
from django.views import generic
from .models import Category, ProductItem
from .serializers import CategoriesSerializer, ProductItemsSerializer


# class CategoriesView(APIView):
#     # queryset = Category.objects.all()
#     queryset = get_list_or_404(Category)
#     serializer_class = CategoriesSerializer

# class CategoriesView(APIView):
#     def get(self, request):
#         categories = get_list_or_404(Category)
#         serializer = CategoriesSerializer(categories, many=True)
#         return Response(serializer.data, status=200)

# class CategoriesView(ListAPIView):
#     queryset = Category.objects.all()
#     # queryset = get_list_or_404(Category)
#     serializer_class = CategoriesSerializer


# class ProductItemsView(ListAPIView):
#     queryset = ProductItem.objects.all()
#     serializer_class = ProductItemsSerializer


class CategoriesView(generic.ListView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class ProductItemsView(generic.ListView):
    queryset = ProductItem.objects.all()
    serializer_class = ProductItemsSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return ProductItem.objects.filter(category_id=category_id)
