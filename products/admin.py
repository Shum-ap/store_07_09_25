from django.contrib import admin
from .models import Category, Supplier, Product, ProductDetail, Address, Customer, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone_number')
    search_fields = ('name', 'contact_email', 'phone_number')
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'supplier',
        'price',
        'quantity',
        'article',
        'available'
    ]
    list_filter = ['category', 'supplier', 'available']
    search_fields = ['name', 'article']
    ordering = ['category', 'quantity']
    list_editable = ['price', 'quantity', 'available']


@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'weight', 'dimensions', 'color')
    search_fields = ('product__name',)
    list_filter = ('color',)
    # Добавим возможность редактировать поля в списке
    list_editable = ['weight', 'dimensions', 'color']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street', 'house')
    search_fields = ('country', 'city', 'street', 'house')
    ordering = ('country', 'city', 'street')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'date_joined',
        'deleted'
    )
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    ordering = ('-date_joined',)
    list_filter = ('deleted',)
    list_editable = ('deleted',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    # Улучшим отображение
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('price',)  # Цена может быть автоматически заполнена


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'order_date', 'customer')
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__email')
    ordering = ('-order_date',)
    # Добавим фильтр по дате заказа
    list_filter = ('order_date',)