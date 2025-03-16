import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QGridLayout, QMessageBox, QGroupBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from main import Main_Ui

# Hàm kết nối database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ql_truyen"
    )

# Lớp giao diện đăng nhập
class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng nhập")
        self.setGeometry(500, 200, 400, 300)
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # Tiêu đề
        title = QLabel("QUẢN LÝ THUÊ BÁN TRUYỆN")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Group Box chứa form đăng nhập
        group_box = QGroupBox("Đăng nhập")
        group_layout = QGridLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.username_input.setFont(QFont("Arial", 12))
        group_layout.addWidget(QLabel("Tên đăng nhập:"), 0, 0)
        group_layout.addWidget(self.username_input, 0, 1)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Arial", 12))
        group_layout.addWidget(QLabel("Mật khẩu:"), 1, 0)
        group_layout.addWidget(self.password_input, 1, 1)

        self.login_button = QPushButton("Đăng nhập", self)
        self.login_button.setFont(QFont("Arial", 12))
        self.login_button.clicked.connect(self.login)
        group_layout.addWidget(self.login_button, 2, 0, 1, 2)

        self.register_button = QPushButton("Đăng ký")
        self.register_button.clicked.connect(self.open_register)
        self.forgot_password_button = QPushButton("Quên mật khẩu")
        self.forgot_password_button.clicked.connect(self.open_reset_password)

        group_layout.addWidget(self.register_button, 3, 0)
        group_layout.addWidget(self.forgot_password_button, 3, 1)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbtaikhoan WHERE tennguoidung = %s AND matkhau = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            QMessageBox.information(self, "Thành công", "Đăng nhập thành công!")
            self.main_ui = Main_Ui()
            self.main_ui.show()
            self.close()
        else:
            QMessageBox.warning(self, "Lỗi", "Sai tài khoản hoặc mật khẩu.")

    def open_main(self):
        QMessageBox.information(self, "Thông báo", "Chuyển sang main.py")

    def open_register(self):
        self.register_form = RegisterForm()
        self.register_form.show()

    def open_reset_password(self):
        self.reset_form = ResetPasswordForm()
        self.reset_form.show()

# Lớp giao diện đăng ký
class RegisterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng ký tài khoản")
        self.setGeometry(500, 200, 400, 350)
        self.setFixedSize(400, 350)

        layout = QVBoxLayout()
        group_box = QGroupBox("Đăng ký")
        group_layout = QGridLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Số điện thoại")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        group_layout.addWidget(QLabel("Tên đăng nhập:"), 0, 0)
        group_layout.addWidget(self.username_input, 0, 1)
        group_layout.addWidget(QLabel("Email:"), 1, 0)
        group_layout.addWidget(self.email_input, 1, 1)
        group_layout.addWidget(QLabel("Số điện thoại:"), 2, 0)
        group_layout.addWidget(self.phone_input, 2, 1)
        group_layout.addWidget(QLabel("Mật khẩu:"), 3, 0)
        group_layout.addWidget(self.password_input, 3, 1)

        self.register_button = QPushButton("Đăng ký")
        self.register_button.clicked.connect(self.register)
        group_layout.addWidget(self.register_button, 4, 0, 1, 2)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        password = self.password_input.text()

        if not username or not email or not phone or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO tbtaikhoan (tennguoidung, email, sodienthoai, matkhau) VALUES (%s, %s, %s, %s)", 
                           (username, email, phone, password))
            conn.commit()
            QMessageBox.information(self, "Thành công", "Đăng ký thành công!")
            self.close()
        except mysql.connector.Error as err:
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi đăng ký: {err}")
        finally:
            conn.close()

# Lớp giao diện quên mật khẩu
class ResetPasswordForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quên mật khẩu")
        self.setGeometry(500, 200, 400, 250)
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()
        group_box = QGroupBox("Đặt lại mật khẩu")
        group_layout = QGridLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.new_password_input = QLineEdit(self)
        self.new_password_input.setPlaceholderText("Mật khẩu mới")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        group_layout.addWidget(QLabel("Tên đăng nhập:"), 0, 0)
        group_layout.addWidget(self.username_input, 0, 1)
        group_layout.addWidget(QLabel("Mật khẩu mới:"), 1, 0)
        group_layout.addWidget(self.new_password_input, 1, 1)

        self.reset_button = QPushButton("Đặt lại mật khẩu")
        self.reset_button.clicked.connect(self.reset_password)
        group_layout.addWidget(self.reset_button, 2, 0, 1, 2)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        self.setLayout(layout)

    def reset_password(self):
        username = self.username_input.text()
        new_password = self.new_password_input.text()

        if not username or not new_password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đủ thông tin!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbtaikhoan WHERE tennguoidung = %s", (username,))
        user = cursor.fetchone()

        if not user:
            QMessageBox.warning(self, "Lỗi", "Tài khoản không tồn tại!")
        else:
            cursor.execute("UPDATE tbtaikhoan SET matkhau = %s WHERE tennguoidung = %s", (new_password, username))
            conn.commit()
            QMessageBox.information(self, "Thành công", "Mật khẩu đã được cập nhật!")
            self.close()
        conn.close()

# Chạy ứng dụng
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec())
