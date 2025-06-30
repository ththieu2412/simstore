# 🛒 **Xây Dựng Website Kinh Doanh Sim Điện Thoại**

Dự án **SimStore** là một nền tảng thương mại điện tử đơn giản, hỗ trợ người dùng duyệt, đặt mua sim điện thoại và thanh toán trực tuyến (hoặc tiền mặt). Hệ thống cũng hỗ trợ quản trị viên trong việc quản lý sản phẩm, đơn hàng và báo cáo doanh thu.
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

SimStore là một website bán sim điện thoại, cung cấp các chức năng chính:

- Xem danh sách sim đang bán theo danh mục

- Đặt hàng và thanh toán (tiền mặt hoặc online)

- Quản lý đơn hàng, nhân viên

- Thống kê doanh thu, tình trạng đơn hàng

Mục tiêu là tạo ra một hệ thống trực quan, dễ sử dụng cho cả người dùng và quản trị viên.

---

## 🛠️ **Công Nghệ Sử Dụng**

- **Backend**: Django (Python)
- **Cơ Sở Dữ Liệu**: MySQL
- **Xử lý API**: Django Rest Framework
- **Bảo mật**: JWT Authentication,CSRF,CORS

---

## 📝 **Cài Đặt**

### Yêu Cầu Hệ Thống
- Python 3.8
- MySQL

### Cài Đặt Dự Án
1. **Clone dự án**:
   ```bash
   git clone https://github.com/ththieu2412/simstore.git
   cd be
   cd simstore

2. **Cài đặt các thư viện yêu cầu: Cài đặt các gói Python bằng pip:**
   ```bash
   pip install -r requirements.txt

3. **Cài đặt MySQL:**
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

- Quản lý Sim: Thêm, sửa, xóa, tìm kiếm sim
- Đặt hàng và thanh toán: Người dùng có thể thực hiện các đơn hàng, và hệ thống sẽ xử lý thanh toán thông qua API payment.
- Quản lý đơn hàng: Nhân viên có thể xem và quản lý tất cả đơn hàng.
- Xác thực JWT: Đăng nhập/đăng ký, phân quyền.
- Thống kê báo cáo: Doanh thu, đơn hàng theo trạng thái, thời gian.

---

## 🛠️ Quá Trình Phát Triển
### 1. **Lập kế hoạch và thiết kế cơ sở dữ liệu**
- Định nghĩa các bảng cơ sở dữ liệu như Sim, Order, Customer, Account, v.v.
- Thiết kế các mối quan hệ giữa các bảng (One-to-Many, Many-to-Many).

### 2. **Phát triển API với Django Rest Framework**
- Xây dựng các API cho các chức năng như quản lý đơn hàng, thanh toán.

### 4. Kiểm thử và triển khai
- Viết các bài kiểm thử cho các chức năng của hệ thống.

---

## 📞 Liên Hệ
Nếu bạn có bất kỳ câu hỏi hoặc đề xuất nào, vui lòng liên hệ qua:
- Email: ththieu2412@gmail.com
- GitHub: https://github.com/ththieu2412
