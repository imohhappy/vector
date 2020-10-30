from django.contrib import admin
from .models import Category, Product, Order, OrderItem

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image', 'overview')
    perpopulated_fields = {'slug': ('name')}


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'postal_code', 'city', 'paid', ]
    list_filter = ['paid']
    inlines = [OrderItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('name', 'price')
    perpopulated_fields = {'slug': ('name',)}
