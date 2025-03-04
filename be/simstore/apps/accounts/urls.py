from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, AccountViewSet, RoleViewSet, LogoutView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    path("", include(router.urls)), 
    path('account/logout/', LogoutView.as_view(), name='logout'),
]
