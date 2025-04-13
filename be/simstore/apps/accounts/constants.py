PHONE_NUMBER_REGEX = r"^\d{10,15}$"
PHONE_NUMBER_ERROR = "Số điện thoại không hợp lệ (phải từ 10 đến 15 chữ số)."

CITIZEN_ID_LENGTH = 12
CITIZEN_ID_ERROR = "CCCD bắt buộc 12 ký tự số."

MIN_AGE_YEARS = 15
DATE_OF_BIRTH_ERROR_FUTURE = "Ngày sinh không hợp lệ."
DATE_OF_BIRTH_ERROR_AGE = f"Nhân viên phải lớn hơn {MIN_AGE_YEARS} tuổi."

MAX_AVATAR_SIZE_MB = 5
AVATAR_SIZE_ERROR = f"Kích thước ảnh phải nhỏ hơn {MAX_AVATAR_SIZE_MB}MB."

PASSWORD_MIN_LENGTH = 8
PASSWORD_ERROR_LENGTH = f"Mật khẩu phải có ít nhất {PASSWORD_MIN_LENGTH} ký tự."
PASSWORD_ERROR_DIGIT = "Mật khẩu phải chứa ít nhất một số."
PASSWORD_ERROR_UPPERCASE = "Mật khẩu phải chứa ít nhất một chữ hoa."
PASSWORD_ERROR_LOWERCASE = "Mật khẩu phải chứa ít nhất một chữ thường."
PASSWORD_ERROR_SPECIAL = "Mật khẩu phải chứa ít nhất một ký tự đặc biệt."
SPECIAL_CHARACTERS = "!@#$%^&*()_+-=[]{}|;:'\",.<>?/"