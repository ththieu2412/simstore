from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """Xử lý lỗi và format lại theo ý muốn"""
    response = exception_handler(exc, context)

    # Nếu lỗi là User bị vô hiệu hóa
    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        if response.data.get("detail") == "User is inactive":
            return Response({
                "statuscode": status.HTTP_403_FORBIDDEN,
                "data": None,
                "status": "error",
                "errorMessage": "Tài khoản đã bị vô hiệu hóa!"
            }, status=status.HTTP_403_FORBIDDEN)

    return response
