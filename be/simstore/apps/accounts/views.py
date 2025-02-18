from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import EmployeeSerializer, AccountSerializer
from models import Employee, Account
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "statuscode": status.HTTP_201_CREATED,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                "statuscode": status.HTTP_200_OK,
                "data": serializer.data,
                "status": "success",
                "errorMessage": None
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "statuscode": status.HTTP_400_BAD_REQUEST,
                "data": None,
                "status": "error",
                "errorMessage": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer