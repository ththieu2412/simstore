from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Định tuyến cho API
    path('', include(router.urls)),
]
