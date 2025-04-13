# Trạng thái đơn hàng
ORDER_STATUS_CANCELLED = 0
ORDER_STATUS_CONFIRMED = 1
ORDER_STATUS_SHIPPING = 2
ORDER_STATUS_COMPLETED = 3
ORDER_STATUS_CHOICES = [
    (ORDER_STATUS_CANCELLED, "Đã hủy"),
    (ORDER_STATUS_CONFIRMED, "Chờ xác nhận"),
    (ORDER_STATUS_SHIPPING, "Đang giao hàng"),
    (ORDER_STATUS_COMPLETED, "Đã giao hàng"),
]

# Trạng thái cập nhật đơn hàng
DETAIL_UPDATE_STATUS_CANCELLED = 0
DETAIL_UPDATE_STATUS_SHIPPING = 2
DETAIL_UPDATE_STATUS_COMPLETED = 3
DETAIL_UPDATE_STATUS_CHOICES = [
    (DETAIL_UPDATE_STATUS_CANCELLED, "Đã hủy"),
    (DETAIL_UPDATE_STATUS_SHIPPING, "Đang giao hàng"),
    (DETAIL_UPDATE_STATUS_COMPLETED, "Đã giao hàng"),
]

# Trạng thái thanh toán
PAYMENT_STATUS_UNPAID = 0
PAYMENT_STATUS_PAID = 1
PAYMENT_STATUS_CHOICES = [
    (PAYMENT_STATUS_UNPAID, "Chưa thanh toán"),
    (PAYMENT_STATUS_PAID, "Đã thanh toán"),
]

# Phương thức thanh toán
PAYMENT_METHOD_CASH = "cash"
PAYMENT_METHOD_TRANSFER = "transfer"
PAYMENT_METHOD_CHOICES = [
    (PAYMENT_METHOD_CASH, "Tiền mặt"),
    (PAYMENT_METHOD_TRANSFER, "Chuyển khoản"),
]

# Trạng thái giảm giá
DISCOUNT_STATUS_UNUSED = False
DISCOUNT_STATUS_USED = True
DISCOUNT_STATUS_CHOICES = [
    (DISCOUNT_STATUS_UNUSED, "Chưa sử dụng"),
    (DISCOUNT_STATUS_USED, "Đã sử dụng"),
]