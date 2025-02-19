from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, ImportReceiptViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'import-receipts', ImportReceiptViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
