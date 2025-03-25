from django.urls import path
from .views import MonthlyRevenueReport

urlpatterns = [
    path('monthly-revenue/', MonthlyRevenueReport.as_view(), name='monthly_revenue_report'),
]
