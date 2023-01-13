from rest_framework import serializers
from .models import Category, ProductItem


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductItemsSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    image = serializers.SerializerMethodField()


    def get_image(self, data):
        request = self.context.get("request")
        if data.image:
            return request.build_absolute_uri(data.image.url)
        return None

    class Meta:
        model = ProductItem
        fields = ('id', 'name', 'description', 'price', 'category', 'image')
