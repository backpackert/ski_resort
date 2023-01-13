from rest_framework import serializers
from .models import EquipCategory, EquipItem, RegisteredUser, Order
from django.contrib.auth import authenticate
from django.utils import timezone


class EquipCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipCategory
        fields = '__all__'


class EquipItemsSerializer(serializers.ModelSerializer):
    category = EquipCategoriesSerializer()
    image = serializers.SerializerMethodField()

    def get_image(self, data):
        request = self.context.get("request")
        if data.image:
            return request.build_absolute_uri(data.image.url)
        return None

    class Meta:
        model = EquipItem
        fields = ['id', 'name', 'description', 'price', 'count_on_stock', 'category', 'image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser
        fields = ['login', 'phone', 'password', 'sex']


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = RegisteredUser
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['phone', 'login', 'password', 'token', 'email',]

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return RegisteredUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=255, style={'placeholder': 'phone', 'autofocus': True})
    password = serializers.CharField(max_length=128, write_only=True, style={'input_type': 'password', 'placeholder': 'Password'})
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone = data.get('phone', None)
        password = data.get('password', None)

        if phone is None:
            raise serializers.ValidationError('An phone number is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=phone, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
            'phone': user.phone,
            'token': user.token
        }


class AddProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    number_of_items = serializers.IntegerField()


class ProductInBasketSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    number_of_items = serializers.IntegerField()
    number_of_days = serializers.IntegerField()


class BasketSerializer(serializers.Serializer):
    products = ProductInBasketSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    total_rental_days = serializers.SerializerMethodField()
    start_rental_day = serializers.DateField(format='%d.%m.%Y', input_formats=['%d.%m.%Y', 'iso-8601', ])
    end_rental_day = serializers.DateField(format='%d.%m.%Y', input_formats=['%d.%m.%Y', 'iso-8601', ])

    def get_total_rental_days(self, data):
        total_rental_days = (data.end_rental_day - data.start_rental_day).days
        return total_rental_days

    def get_total_price(self, data):
        total_price = 0

        for item in data.get('products'):
            total_price += (item.get('price') * item.get('number_of_items') * item.get('number_of_days'))
        return total_price


class CreateOrderSerializer(serializers.ModelSerializer):
    def run_validation(self, data=None):
        return data

    class Meta:
        model = Order
        fields = '__all__'

    def calculate_total_price(self, data):
        product_items_dict = data.get('product_items')
        product_items_ids = product_items_dict.keys()
        product_items = EquipItem.objects.filter(id__in=product_items_ids).values('id', 'name', 'price')
        total_price = 0

        for item in product_items:
            number_of_items = product_items_dict.get(str(item.get('id')))
            price = item.get('price')

            total_price += price * number_of_items

        user = self.context.get('request').user
        user.save()
        return total_price

    def get_total_number_of_items(self, data):
        return sum(data.get('product_items').values())

    def get_user(self):
        request = self.context.get('request')
        return request.user

    def create(self, validated_data):
        validated_data['total_price'] = self.calculate_total_price(validated_data)
        validated_data['total_number_of_items'] = self.get_total_number_of_items(validated_data)
        validated_data['user'] = self.get_user()
        return Order.objects.create(**validated_data)


class DeleteProductSerializer(serializers.Serializer):
    product_item_id = serializers.IntegerField()
