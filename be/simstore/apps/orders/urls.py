from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, CustomerViewSet, PaymentViewSet, DiscountViewSet, create_payment, payment_return, payment_ipn

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r"customers", CustomerViewSet)
router.register(r"payments", PaymentViewSet)
router.register(r"discounts", DiscountViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('payment/create/', create_payment, name='create_payment'),
    path('payment/return/', payment_return, name='payment_return'),
    path('payment/ipn/', payment_ipn, name='payment_ipn'),
]
