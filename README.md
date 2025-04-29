# 🛒 **Xây Dựng Website Thương Mại Điện Tử**

Dự án **Xây dựng website thương mại điện tử** được phát triển với mục tiêu tạo ra một nền tảng mua bán trực tuyến, cho phép người dùng có thể duyệt, đặt hàng và thanh toán trực tuyến một cách dễ dàng. Dự án bao gồm các chức năng chính như quản lý khách hàng, đơn hàng, thanh toán và quản lý sản phẩm.

---

## 📑 Mục Lục
1. [Giới thiệu](#giới-thiệu)
2. [Công Nghệ Sử Dụng](#công-nghệ-sử-dụng)
3. [Cài Đặt](#cài-đặt)
4. [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
5. [Tính Năng](#tính-năng)
6. [Quá Trình Phát Triển](#quá-trình-phát-triển)
7. [Cách Thức Triển Khai](#cách-thức-triển-khai)
8. [Liên Hệ](#liên-hệ)

---

## 🚀 **Giới Thiệu**

Dự án này là một hệ thống thương mại điện tử cho phép người dùng thực hiện các hành động sau:
- Đăng ký và đăng nhập tài khoản người dùng
- Duyệt các sản phẩm và thêm vào giỏ hàng
- Quản lý đơn hàng
- Hỗ trợ thanh toán và giao hàng
- Quản lý thông tin khách hàng, đơn hàng và sản phẩm từ phía admin

Mục tiêu của dự án là xây dựng một website đơn giản nhưng đầy đủ các tính năng cơ bản của một website thương mại điện tử, đồng thời tối ưu hóa trải nghiệm người dùng và quản lý hệ thống dễ dàng cho admin.

---

## 🛠️ **Công Nghệ Sử Dụng**

- **Backend**: Django (Python)
- **Frontend**: ReactJS (Optional for frontend)
- **Cơ Sở Dữ Liệu**: MySQL
- **Xử lý API**: Django Rest Framework
- **Bảo mật**: JWT Authentication, HTTPS

---

## 📝 **Cài Đặt**

### Yêu Cầu Hệ Thống
- Python 3.x
- MySQL

### Cài Đặt Dự Án
1. **Clone dự án**:
   ```bash
   git clone https://github.com/yourusername/ecommerce-website.git
   cd ecommerce-website

2. **Cài đặt các thư viện yêu cầu: Cài đặt các gói Python bằng pip:**
   ```bash
   pip install -r requirements.txt

3. **Cài đặt PostgreSQL:**
  - Đảm bảo đã cài đặt MySQL và tạo một cơ sở dữ liệu cho dự án.
  - Cấu hình thông tin kết nối trong file settings.py.

4. **Chạy migrations: Sau khi cài đặt, chạy migrations để tạo các bảng trong cơ sở dữ liệu:**
   ```bash
   python manage.py migrate

5. **Chạy server: Để chạy server development:**
   ```bash
   python manage.py runserver

--- 

## 🔑 Tính Năng
- Quản lý sản phẩm: Admin có thể thêm, sửa, xóa sản phẩm từ hệ thống.
- Giỏ hàng: Người dùng có thể thêm sản phẩm vào giỏ hàng và tiến hành thanh toán.
- Đặt hàng và thanh toán: Người dùng có thể thực hiện các đơn hàng, và hệ thống sẽ xử lý thanh toán thông qua API payment.
- Quản lý đơn hàng: Nhân viên có thể xem và quản lý tất cả đơn hàng.
- Thông báo và Email: Hệ thống gửi thông báo và email khi đơn hàng được xử lý.

---

## 🛠️ Quá Trình Phát Triển
### 1. **Lập kế hoạch và thiết kế cơ sở dữ liệu**
- Định nghĩa các bảng cơ sở dữ liệu như Sim, Order, Customer, Account, v.v.
- Thiết kế các mối quan hệ giữa các bảng (One-to-Many, Many-to-Many).

### 2. **Phát triển API với Django Rest Framework**
- Xây dựng các API cho các chức năng như quản lý đơn hàng, thanh toán.

### 3. Tạo giao diện người dùng
- Sử dụng ReactJS để xây dựng giao diện web.

### 4. Kiểm thử và triển khai
- Viết các bài kiểm thử cho các chức năng của hệ thống.

---

## 📞 Liên Hệ
Nếu bạn có bất kỳ câu hỏi hoặc đề xuất nào, vui lòng liên hệ qua:
- Email: ththieu2412@gmail.com
- GitHub: https://github.com/ththieu2412
