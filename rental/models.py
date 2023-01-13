from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import jwt
from django.conf import settings
import uuid
from datetime import datetime, timedelta, date
from django.utils import timezone

user = settings.AUTH_USER_MODEL


SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)


class EquipCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/equipcategories', null=True, blank=True, default=None)

    def __str__(self):  # метод строковой репрезентации в админке, чтобы красиво отображалось
        return self.name # будет возвращать только имя

    class Meta:
        verbose_name = 'Equipment category'
        verbose_name_plural = 'Equipment categories'


class EquipItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count_on_stock = models.IntegerField()
    image = models.ImageField(upload_to='media/equipment', null=True, blank=True, default=None)
    category = models.ForeignKey(EquipCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Equip item'
        verbose_name_plural = 'Equip items'


class UserManager(BaseUserManager):
    def create_user(self, password, phone, email,
                    is_admin=False, is_staff=False, is_active=True, login=''):

        if not phone:
            raise ValueError("User must have a phone number")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(phone=phone)
        user.set_password(password)
        user.email = email
        user.login = login
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.is_superuser = False
        user.save()

        return user

    def create_superuser(self, password, phone, email):
        if not phone:
            raise ValueError("User must have a phone number")
        if not password:
            raise ValueError("User must have a password")

        user = self.create_user(password, email, phone, is_admin=True, is_staff=True, is_active=True)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.email = email
        user.save()
        return user


class RegisteredUser(AbstractUser):
    username = None
    email = models.EmailField(default=None)
    sex = models.CharField(choices=SEX_CHOICES, max_length=20, default='M')
    phone = models.CharField(max_length=20, unique=True)
    login = models.CharField(max_length=100, default='')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.login

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class Basket(models.Model):
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    product = models.ForeignKey(EquipItem, on_delete=models.CASCADE)
    number_of_items = models.IntegerField(blank=True, null=True)
    number_of_days = models.IntegerField(blank=True, null=True)
    start_rental_day = models.DateField(default=date.today)
    end_rental_day = models.DateField(default=date.today)


class Order(models.Model):
    RENTAL_STATUSES = (('Booked', 'Booked'),
                       ('Not confirmed', 'Not confirmed'))

    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_number_of_items = models.IntegerField()
    product_items = models.JSONField()
    start_rental_day = models.DateField(default=date.today, null=True, blank=True)
    end_rental_day = models.DateField(default=date.today, null=True, blank=True)
    total_rental_days = models.IntegerField()
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUSES, blank=True,
                                     help_text='Order status')
