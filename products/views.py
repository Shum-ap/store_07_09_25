from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Supplier, Product, ProductDetail, Address, Customer, Order, OrderItem
from products.serializers import (
    CategorySerializer,
    SupplierSerializer,
    ProductSerializer,
    ProductCreateUpdateSerializer,
    ProductDetailSerializer,
    ProductDetailCreateUpdateSerializer,
    AddressSerializer,
    CustomerSerializer,
    CustomerCreateUpdateSerializer,
    OrderSerializer,
    OrderCreateUpdateSerializer,
    OrderItemSerializer,
    OrderItemCreateUpdateSerializer,
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'price']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

class ProductDetailViewSet(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductDetailCreateUpdateSerializer
        return ProductDetailSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CustomerCreateUpdateSerializer
        return CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderCreateUpdateSerializer
        return OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderItemCreateUpdateSerializer
        return OrderItemSerializer