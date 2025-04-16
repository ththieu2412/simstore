import hmac
import hashlib
import urllib.parse

secret = "YOUR_HASH_SECRET"  # Thay bằng VNPAY_HASH_SECRET
query_string = "vnp_Amount=60000000&vnp_Command=pay&vnp_CreateDate=20250416162454&vnp_CurrCode=VND&vnp_IpAddr=127.0.0.1&vnp_Locale=vn&vnp_OrderInfo=Thanh+to%C3%A1n+sim+0845458221125&vnp_OrderType=telco&vnp_ReturnUrl=http%3A%2F%2Flocalhost%3A8000.com%2Fpayment%2Freturn%2F&vnp_TmnCode=R0HSENCZ&vnp_TxnRef=12&vnp_Version=2.1.0&vnp_SecureHash=647aca7328b5a6d701442d99291224690511c1bbef20d5fb8ce2058fbccf0c1da09a930abbad0a181c7b175efcef5cad4febfc1c8ded1f7f3176a2ee886caffd"
hash_data = query_string.encode('utf-8')
secure_hash = hmac.new(secret.encode('utf-8'), hash_data, hashlib.sha512).hexdigest()
print(secure_hash)