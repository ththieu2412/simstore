from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, AccountViewSet, RoleViewSet, LogoutView, PasswordResetRequestView, PasswordResetConfirmView, CustomTokenRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'accounts', AccountViewSet)
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    path("", include(router.urls)), 
    path('account/logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
