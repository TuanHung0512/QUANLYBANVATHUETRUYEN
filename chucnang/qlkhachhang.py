import sys
import mysql.connector
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QLabel, QPushButton, QVBoxLayout

class FormKhachHang(QtWidgets.QDialog):
    def __init__(self, parent=None, makhach="", tenkhach="", tuoi="", gioitinh="", sodienthoai="", diachi=""):
        super(FormKhachHang, self).__init__(parent)
        self.setWindowTitle("Thông tin khách hàng")

        layout = QVBoxLayout()
        
        self.lineEditMaKhach = QLineEdit(makhach)
        self.lineEditTenKhach = QLineEdit(tenkhach)
        self.lineEditTuoi = QLineEdit(tuoi)
        self.lineEditGioiTinh = QLineEdit(gioitinh)
        self.lineEditSoDienThoai = QLineEdit(sodienthoai)
        self.lineEditDiaChi = QLineEdit(diachi)
        self.btnLuu = QPushButton("Lưu")
        self.btnHuy = QPushButton("Hủy")
        
        layout.addWidget(QLabel("Mã Khách"))
        layout.addWidget(self.lineEditMaKhach)
        layout.addWidget(QLabel("Tên Khách"))
        layout.addWidget(self.lineEditTenKhach)
        layout.addWidget(QLabel("Tuổi"))
        layout.addWidget(self.lineEditTuoi)
        layout.addWidget(QLabel("Giới Tính"))
        layout.addWidget(self.lineEditGioiTinh)
        layout.addWidget(QLabel("Số Điện Thoại"))
        layout.addWidget(self.lineEditSoDienThoai)
        layout.addWidget(QLabel("Địa Chỉ"))
        layout.addWidget(self.lineEditDiaChi)

        layout.addWidget(self.btnLuu)
        layout.addWidget(self.btnHuy)
        
        self.setLayout(layout)
        
        self.btnLuu.clicked.connect(self.accept)
        self.btnHuy.clicked.connect(self.reject)
    
    
    def get_data(self):
        return (
            self.lineEditMaKhach.text(),
            self.lineEditTenKhach.text(),
            self.lineEditTuoi.text(),
            self.lineEditGioiTinh.text(),
            self.lineEditSoDienThoai.text(),
            self.lineEditDiaChi.text(),
        )

class QLKH(QtWidgets.QMainWindow):
    def __init__(self, parent= None):
        super(QLKH, self).__init__()
        uic.loadUi("giaodien/qlkh.ui", self)
        self.parent = parent
        self.connect_database()
        self.load_data()
        
        self.btn_themkh.clicked.connect(self.them_kh)
        self.btn_suakh.clicked.connect(self.sua_kh)
        self.btn_xoakh.clicked.connect(self.xoa_kh)
        self.btn_timkiemkh.clicked.connect(self.tim_kiem_kh)
        self.btn_quaylai2.clicked.connect(self.quay_lai2)

    def quay_lai2(self):
        from main import Main_Ui
        self.hide()
        self.main_ui = Main_Ui()
        self.main_ui.show()
        
    def connect_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ql_truyen"
                    # Sửa thành dbbanhang theo ảnh
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối cơ sở dữ liệu: {e}")
    
    def load_data(self):
        query = "SELECT makhach, tenkhach, tuoi, gioitinh, sodienthoai, diachi FROM tbkhachhang"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.fill_table(rows)
    
    def fill_table(self, rows):
        self.tableWidget.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_data in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(cell_data)))
    
    def them_kh(self):
        form = FormKhachHang(self)
        if not form.exec():  # Nếu form bị hủy, thoát khỏi hàm
            return
        
        if form.exec():
            makhach, tenkhach, tuoi, gioitinh, sodienthoai, diachi = form.get_data()
        
        # Kiểm tra nếu có trường nào bị bỏ trống
        if not all([makhach, tenkhach, tuoi, gioitinh, sodienthoai, diachi]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Kiểm tra trùng mã truyện
        self.cursor.execute("SELECT COUNT(*) FROM tbkhachhang WHERE makhach = %s", (makhach,))
        if self.cursor.fetchone()[0] > 0:
            QMessageBox.warning(self, "Lỗi", "Mã khách hàng đã tồn tại!")
            return
        
        # Kiểm tra trùng tên truyện
        self.cursor.execute("SELECT COUNT(*) FROM tbkhachhang WHERE tenkhach = %s", (tenkhach,))
        if self.cursor.fetchone()[0] > 0:
            QMessageBox.warning(self, "Lỗi", "Tên khách hàng đã tồn tại!")
            return
        
        query = "INSERT INTO tbkhachhang (makhach, tenkhach, tuoi, gioitinh, sodienthoai, diachi) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (makhach, tenkhach, tuoi, gioitinh, sodienthoai, diachi))
        self.db.commit()
        self.load_data()
        QMessageBox.information(self, "Thành công", "Thêm khách hàng thành công!")

    def sua_kh(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
           makhach = self.tableWidget.item(selected_row, 0).text()
           tenkhach_cu = self.tableWidget.item(selected_row, 1).text()

        form = FormKhachHang(self, makhach, tenkhach_cu)
        if form.exec():
            tenkhach_moi, tuoi, gioitinh, sodienthoai, diachi = form.get_data()[1:]

            # Kiểm tra trùng tên truyện (trừ chính nó)
            self.cursor.execute("SELECT COUNT(*) FROM tbkhachhang WHERE tenkhach = %s AND makhach != %s", (tenkhach_moi, makhach))
            if self.cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Lỗi", "Tên khách hàng đã tồn tại!")
                return

            query = "UPDATE tbkhachhang SET tenkhach=%s, tuoi=%s, gioitinh=%s, sodienthoai=%s, diachi=%s WHERE makhach=%s"
            self.cursor.execute(query, (tenkhach_moi, tuoi, gioitinh, sodienthoai, diachi, makhach))
            self.db.commit()
            self.load_data()
            QMessageBox.information(self, "Thành công", "Sửa thông tin thành công!")


    def xoa_kh(self):
        if not hasattr(self, "tableWidget"):
            return
        
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            mahang = self.tableWidget.item(selected_row, 0).text()
            confirm = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa thông tin khách hànghàng này?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                query = "DELETE FROM tbkhachhang WHERE makhach=%s"
                self.cursor.execute(query, (mahang,))
                self.db.commit()
                self.load_data()
                QMessageBox.information(self, "Thành công", "Xóa khách hàng thành công!")

    def tim_kiem_kh(self):
        if not hasattr(self, "lineEditTenKhachHang"):
            return

        line_edit = self.findChild(QLineEdit, "lineEditTenKhachHang")
        if line_edit is None:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy ô nhập liệu tìm kiếm!")
            return
        
        tenkhach = line_edit.text()
        query = "SELECT makhach, tenkhach, tuoi, gioitinh, sodienthoai, diachi FROM tbkhachhang WHERE tenkhach LIKE %s"
        self.cursor.execute(query, ("%" + tenkhach + "%",))
        rows = self.cursor.fetchall()
        self.fill_table(rows)
        QMessageBox.information(self, "Kết quả", f"Tìm thấy {len(rows)} kết quả!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QLKH()
    window.show()
    sys.exit(app.exec())