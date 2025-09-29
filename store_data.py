
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist

# Импортируем модели из приложения products
from products.models import Category, Product, Supplier, Customer, Order, OrderItem, Address

def export_data():
    # Очистим старые данные (опционально)
    Product.objects.all().delete()
    Category.objects.all().delete()
    Supplier.objects.all().delete()
    Customer.objects.all().delete()
    Order.objects.all().delete()
    Address.objects.all().delete()

    # === Категории ===
    electronics = Category.objects.create(name="Электроника")
    clothes = Category.objects.create(name="Одежда")

    # === Поставщики ===
    tech_supply = Supplier.objects.create(
        name="TechSupply",
        contact_email="tech@supply.com"
    )
    fashion_house = Supplier.objects.create(
        name="FashionHouse",
        contact_email="fashion@house.com"
    )

    # === Продукты ===
    smartphone = Product.objects.create(
        name="Смартфон",
        price=30000,
        quantity=50,
        category=electronics,
        supplier=tech_supply
    )
    laptop = Product.objects.create(
        name="Ноутбук",
        price=60000,
        quantity=20,
        category=electronics,
        supplier=tech_supply
    )
    tshirt = Product.objects.create(
        name="Футболка",
        price=1500,
        quantity=100,
        category=clothes,
        supplier=fashion_house
    )

    # === Адрес клиента ===
    address = Address.objects.create(
        street="Улица Ленина, д. 10",
        city="Москва",
        country="Россия"
    )

    # === Клиент ===
    customer = Customer.objects.create(
        first_name="Иван",
        last_name="Иванов",
        email="ivan@example.com",
        address=address
    )

    # === Заказы ===
    order1 = Order.objects.create(
        customer=customer,
        order_date=date.today() - timedelta(days=5)
    )
    OrderItem.objects.create(
        order=order1,
        product=smartphone,
        quantity=2,
        price=30000
    )
    OrderItem.objects.create(
        order=order1,
        product=tshirt,
        quantity=3,
        price=1500
    )

    order2 = Order.objects.create(
        customer=customer,
        order_date=date.today() - timedelta(days=1)
    )
    OrderItem.objects.create(
        order=order2,
        product=laptop,
        quantity=1,
        price=60000
    )

    print("✅ Данные успешно добавлены в базу!")