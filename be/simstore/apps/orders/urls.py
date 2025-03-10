from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CustomerViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
