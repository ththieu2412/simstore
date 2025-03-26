from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MonthlyRevenueReportViewSet

router = DefaultRouter()
router.register(r'revenue-report', MonthlyRevenueReportViewSet, basename='revenue-report')

urlpatterns = [
    path("", include(router.urls)),
]