from rest_framework import status
from rest_framework.response import Response
from datetime import datetime 

def api_response(status_code, data=None, errors=None):
    """
    Tạo phản hồi API theo định dạng chung.
    
    Args:
        status_code (int): Mã trạng thái HTTP.
        data (dict, optional): Thông báo lỗi hoặc thành công.
        message (str, optional): Thông báo lỗi hoặc thành công.
        errors (dict, optional): Chi tiết lõi nếu có.
    
    Returns:
        Response: Đối tượng phải hồi DRF
    """
    is_success = status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT)
    response_data = {
        "statuscode": status_code,
        "data": data,
        "status": "success" if is_success else "error",
        "errorMessage": errors if not is_success else None,
    }
    return Response(response_data, status=status_code)
