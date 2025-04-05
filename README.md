# 🛒 **Xây Dựng Website Thương Mại Điện Tử**

Dự án **Xây dựng website thương mại điện tử** được phát triển với mục tiêu tạo ra một nền tảng mua bán trực tuyến, cho phép người dùng có thể duyệt, đặt hàng và thanh toán trực tuyến một cách dễ dàng. Dự án bao gồm các chức năng chính như quản lý khách hàng, đơn hàng, giỏ hàng, thanh toán và quản lý sản phẩm.

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
- **Frontend**: HTML, CSS, JavaScript, React (Optional for frontend)
- **Cơ Sở Dữ Liệu**: PostgreSQL
- **Xử lý API**: Django Rest Framework
- **Quản lý phiên làm việc (Session Management)**: Django sessions
- **Bảo mật**: JWT Authentication, HTTPS
- **Triển khai**: Docker, Heroku (cho deployment online)

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

### Triển Khai với Docker (Tùy Chọn)
1. **Xây dựng Docker image:**
  ```bash
  docker build -t ecommerce-website

2. **Chạy ứng dụng qua Docker:**
  ```bash
  docker run -p 8000:8000 ecommerce-website

## 📁 **Cấu Trúc Dự Án**

