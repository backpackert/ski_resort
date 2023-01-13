from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/categories', null=True, blank=True, default=None)

    def __str__(self):  # метод строковой репрезентации в админке, чтобы красиво отображалось
        return self.name # будет возвращать только имя

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/products', null=True, blank=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product item'
        verbose_name_plural = 'Product items'
