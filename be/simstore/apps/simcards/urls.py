from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MobileNetworkOperatorViewSet, Category1ViewSet, Category2ViewSet, SimViewSet

router = DefaultRouter()
router.register(r'mobile-network-operator', MobileNetworkOperatorViewSet)
router.register(r'category1', Category1ViewSet)
router.register(r'category2', Category2ViewSet)
router.register(r'sims', SimViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
