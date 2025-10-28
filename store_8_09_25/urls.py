"""
URL configuration for store_8_09_25 project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка Swagger
schema_view = get_schema_view(
   openapi.Info(
     title="Task Manager API",
     default_version='v1',
     description="API documentation for Task Manager with JWT in httpOnly cookies",
     contact=openapi.Contact(email="contact@snippets.local"),
     license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

from products import views as product_views
from task_manager.views import LoginView, LogoutView

router = DefaultRouter()

# products
router.register(r'suppliers', product_views.SupplierViewSet)
router.register(r'products', product_views.ProductViewSet)
router.register(r'product-details', product_views.ProductDetailViewSet)
router.register(r'addresses', product_views.AddressViewSet)
router.register(r'customers', product_views.CustomerViewSet)
router.register(r'orders', product_views.OrderViewSet)
router.register(r'order-items', product_views.OrderItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),


    path('api/v1/', include(router.urls)),
    path('api/v1/tasks/', include('task_manager.urls')),


    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]