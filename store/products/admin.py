from django.contrib import admin

# Register your models here.
from products.models import Basket, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'category']
    fields = ['image', 'name', 'description', 'specifications', ('price', 'quantity'), 'category', 'is_available']
    readonly_fields = ('is_available',)
    search_fields = ('name',)
    ordering = ('-quantity',)  # сортировка по умолчанию


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0
