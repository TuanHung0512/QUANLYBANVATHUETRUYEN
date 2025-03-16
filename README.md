Hướng Dẫn Cài Đặt và Chạy Chương Trình

1. Yêu Cầu Hệ Thống

Python 3.x

MySQL Server

Visual Studio Code (hoặc bất kỳ IDE nào hỗ trợ Python ví dụ như pychamr)

Các thư viện Python cần thiết (xem phần Cài Đặt)

2. Cấu Trúc Thư Mục

📦 btl/  
 ├── 📄 README.md               # Hướng dẫn sử dụng  
 ├── 📄 Requirements.txt        # Danh sách thư viện cần thiết  
 ├── 📂 chucnang/               # Chứa mã nguồn xử lý logic  
 │   ├── BaoCaoDoanhThu.py  
 │   ├── login.py  
 │   ├── main.py  
 │   ├── qlbantruyen.py  
 │   ├── qlkhachhang.py  
 │   ├── qlthuetruyen.py  
 │   ├── qltruyen.py  
 ├── 📂 database/               # Chứa file CSDL  
 │   ├── ql_truyen.sql  
 ├── 📂 giaodien/               # Chứa giao diện  
 │   ├── baocao.ui  
 │   ├── home.ui  
 │   ├── qlbt.ui  
 │   ├── qlkh.ui  
 │   ├── qlt.ui  
 │   ├── qltt.ui  
 ├── 📂 anhnen/                 # Chứa ảnh nền  
 │   ├── R.jpg  
 
3. Cài Đặt

3.1 Cài Đặt Python và Thư Viện Phụ Thuộc

Cài đặt Python: Tải và cài đặt Python từ python.org hoặc trên microsoft store.

Cài đặt các thư viện cần thiết:

pip install -r Requirements.txt

3.2 Cấu Hình Cơ Sở Dữ Liệu

Tạo database:

Mở MySQL và tạo database mới:

CREATE DATABASE ql_truyen CHARACTER SET utf8 COLLATE utf8_vietnamese_ci;

import file ql_truyen.sql trong thư mục Database để nhập dữ liệu mẫu.

Cập nhật thông tin kết nối trong các file Python:

Mở file có phần kết nối MySQL (chucnang/main.py, chucnang/login.py, .....)

Sửa thông tin user, password, host nếu cần.

4. Chạy Chương Trình

Mở Visual Studio Code.

Ấn file chọn open folder chọn thư mục btl

Chạy chương trình bằng lệnh:

python chucnang/login.py

5. Lưu Ý

Đảm bảo MySQL đang chạy trước khi khởi động chương trình.

Nếu gặp lỗi module không tìm thấy, kiểm tra lại cài đặt thư viện bằng pip list.

Nếu chương trình không kết nối được với MySQL, kiểm tra lại thông tin user/password trong file Python.
