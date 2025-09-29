from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
    article = models.CharField(max_length=100, unique=True, help_text='Unique string product id',db_index=True)
    available = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['category', 'quantity']


class ProductDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='details')
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    dimensions = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)  # ← новое поле

    def __str__(self):
        return f"Details for {self.product.name}"

class Address(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=6)
    def __str__(self):
        return f"{self.street}, {self.house}"
    class Meta:
        verbose_name_plural = 'addresses'


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.OneToOneField(Address, null=True,on_delete=models.SET_NULL, related_name='customer')
    date_joined = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        ordering = ['-date_joined']
        get_latest_by = 'date_joined'


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT,related_name='orders')
    def __str__(self):
        return f"Order {self.id} by {self.customer}"
    class Meta:
        ordering = ['-order_date']
        get_latest_by = 'order_date'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.order}"