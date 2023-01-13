from django.contrib import admin

from .models import Category, ProductItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name', 'category__name')
    list_select_related = ('category', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductItem, ProductItemAdmin)


