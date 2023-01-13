from django.contrib import admin

from .models import EquipCategory, EquipItem, RegisteredUser, Basket, Order


class EquipCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class EquipItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count_on_stock', 'category')
    search_fields = ('name', 'category__name')
    list_select_related = ('category', )


class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'number_of_items', 'number_of_days', 'start_rental_day', 'end_rental_day')
    search_fields = ('user__phone', 'product__name')
    list_select_related = ('user', 'product', )


class RegisteredUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'login', 'email')
    search_fields = ('phone', 'email')


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.get_fields()]


admin.site.register(EquipCategory, EquipCategoryAdmin)
admin.site.register(EquipItem, EquipItemAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(RegisteredUser, RegisteredUserAdmin)
admin.site.register(Order, OrderInfoAdmin)

