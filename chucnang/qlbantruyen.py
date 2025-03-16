import sys
import mysql.connector
from PyQt6 import QtWidgets, uic, QtGui, QtCore
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox


class QLBT(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("giaodien/qlbt.ui", self)  # Load giao diện
        self.conn = mysql.connector.connect(host="localhost", user="root", password="", database="ql_truyen") 
        self.cursor = self.conn.cursor()

        self.load_data()
          
        self.btn_taobt.clicked.connect(self.show_tao_don_ban)
        self.btn_thanhtoan.clicked.connect(self.show_thanh_toan)
        self.btn_ctbt.clicked.connect(self.show_chi_tiet_don_ban)
        self.btn_suabt.clicked.connect(self.show_sua_don_ban)
        self.btn_xoabt.clicked.connect(self.xoa_don_ban)
        self.btn_timkiembt.clicked.connect(self.tim_kiem_don_ban)
        self.btn_quaylai4.clicked.connect(self.quay_lai4)
    
    def quay_lai4(self):
        from main import Main_Ui
        self.hide()
        self.main_ui = Main_Ui()
        self.main_ui.show()
        
    def load_data(self):
        """ Load lại dữ liệu từ database vào tableWidget """
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="ql_truyen")
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT tbdonban.madonban, tbkhachhang.tenkhach, tbdonban.ngayban, tbdonban.tinhtrang 
            FROM tbdonban 
            JOIN tbkhachhang ON tbdonban.makhach = tbkhachhang.makhach
        """)
            rows = cursor.fetchall()
        
            self.tableWidget.clearContents()  # Xóa toàn bộ dữ liệu cũ
            self.tableWidget.setRowCount(0)   # Đặt lại số dòng về 0
            self.tableWidget.setRowCount(len(rows))

            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        
            self.tableWidget.repaint()  # Cập nhật lại giao diện
        
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            cursor.close()
            conn.close()

    def show_tao_don_ban(self):
        """Hiển thị form tạo đơn bán."""
        self.form_tao_don = QtWidgets.QDialog(self)
        self.form_tao_don.setWindowTitle("Tạo Đơn Bán")

        layout = QtWidgets.QVBoxLayout()
        self.txt_madonban = QtWidgets.QLineEdit(self)
        self.txt_makhach = QtWidgets.QLineEdit(self)
        self.txt_ngayban = QtWidgets.QDateEdit(self)
        self.txt_ngayban.setCalendarPopup(True)
        self.txt_tinhtrang = QtWidgets.QLabel("Chưa thanh toán")

        btn_luu = QtWidgets.QPushButton("Lưu", self)
        btn_luu.clicked.connect(self.tao_don_ban)

        layout.addWidget(QtWidgets.QLabel("Mã đơn bán:"))
        layout.addWidget(self.txt_madonban)
        layout.addWidget(QtWidgets.QLabel("Mã khách:"))
        layout.addWidget(self.txt_makhach)
        layout.addWidget(QtWidgets.QLabel("Ngày bán:"))
        layout.addWidget(self.txt_ngayban)
        layout.addWidget(btn_luu)

        self.form_tao_don.setLayout(layout)
        self.form_tao_don.exec()

    def tao_don_ban(self):
        """Thêm đơn bán vào database và hiển thị lên tableWidget, kiểm tra trùng mã đơn bán."""
        madonban = self.txt_madonban.text()
        makhach = self.txt_makhach.text()
        ngayban = self.txt_ngayban.date().toString("yyyy-MM-dd")
        tinhtrang = "Chưa thanh toán"

        if not madonban or not makhach:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            # Kiểm tra xem madonban đã tồn tại chưa
            self.cursor.execute("SELECT COUNT(*) FROM tbdonban WHERE madonban = %s", (madonban,))
            result = self.cursor.fetchone()
            if result[0] > 0:
                QtWidgets.QMessageBox.warning(self, "Lỗi", f"Mã đơn bán {madonban} đã tồn tại. Vui lòng nhập mã khác.")
                return

            # Nếu chưa tồn tại, thêm mới vào database
            self.cursor.execute(
                "INSERT INTO tbdonban (madonban, makhach, ngayban, tinhtrang) VALUES (%s, %s, %s, %s)",
                (madonban, makhach, ngayban, tinhtrang)
            )
            self.conn.commit()
            QtWidgets.QMessageBox.information(self, "Thành công", "Thêm đơn bán thành công!")
        
            self.load_data_table()  # Cập nhật lại bảng hiển thị
            self.form_tao_don.close()
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi tạo đơn bán: {err}")

    def load_data_table(self):
        """Hiển thị danh sách đơn bán lên tableWidget, đổi makhach thành tenkhach."""
        self.cursor.execute("SELECT tbdonban.madonban, tbkhachhang.tenkhach, tbdonban.ngayban, tbdonban.tinhtrang "
                            "FROM tbdonban INNER JOIN tbkhachhang ON tbdonban.makhach = tbkhachhang.makhach")
        rows = self.cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Mã Đơn", "Tên Khách", "Ngày Bán", "Tình Trạng"])

        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col_data)))
    
    def show_thanh_toan(self):
        """Hiển thị form thanh toán khi chọn đơn bán."""
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một đơn bán để thanh toán.")
            return

        madonban = self.tableWidget.item(selected_row, 0).text()

        self.form_thanh_toan = QtWidgets.QDialog(self)
        self.form_thanh_toan.setWindowTitle("Thanh Toán Đơn Bán")

        layout = QtWidgets.QVBoxLayout()
    
        self.txt_machitiet = QtWidgets.QLineEdit(self)
        self.txt_madonban_tt = QtWidgets.QLineEdit(self)
        self.txt_madonban_tt.setText(madonban)
        self.txt_madonban_tt.setReadOnly(True)
        self.txt_matruyen = QtWidgets.QLineEdit(self)
        self.txt_soluong = QtWidgets.QSpinBox(self)
        self.txt_soluong.setMinimum(1)

        # Thay đổi từ QDoubleSpinBox sang QLineEdit + QDoubleValidator
        self.txt_dongia = QtWidgets.QLineEdit(self)
        validator = QtGui.QDoubleValidator(0.00, 9999999.99, 2)  # Chỉ nhập số thực, tối đa 2 số thập phân
        self.txt_dongia.setValidator(validator)
    
        self.txt_thanhtien = QtWidgets.QLabel("0.0")

        self.txt_soluong.valueChanged.connect(self.tinh_thanhtien)
        self.txt_dongia.textChanged.connect(self.tinh_thanhtien)

        btn_luu = QtWidgets.QPushButton("Thanh Toán", self)
        btn_luu.clicked.connect(self.thanh_toan)

        layout.addWidget(QtWidgets.QLabel("Mã chi tiết:"))
        layout.addWidget(self.txt_machitiet)
        layout.addWidget(QtWidgets.QLabel("Mã đơn bán:"))
        layout.addWidget(self.txt_madonban_tt)
        layout.addWidget(QtWidgets.QLabel("Mã truyện:"))
        layout.addWidget(self.txt_matruyen)
        layout.addWidget(QtWidgets.QLabel("Số lượng:"))
        layout.addWidget(self.txt_soluong)
        layout.addWidget(QtWidgets.QLabel("Đơn giá:"))
        layout.addWidget(self.txt_dongia)
        layout.addWidget(QtWidgets.QLabel("Thành tiền:"))
        layout.addWidget(self.txt_thanhtien)
        layout.addWidget(btn_luu)

        self.form_thanh_toan.setLayout(layout)
        self.form_thanh_toan.exec()

    def tinh_thanhtien(self):
        """Tính toán tự động thành tiền."""
        soluong = self.txt_soluong.value()
        try:
            dongia = float(self.txt_dongia.text())  # Lấy giá trị nhập vào dưới dạng số thực
        except ValueError:
            dongia = 0.0  # Nếu giá trị nhập vào không hợp lệ, đặt về 0

        thanhtien = soluong * dongia
        self.txt_thanhtien.setText(f"{thanhtien:.2f}")  # Hiển thị 2 số sau dấu thập phân


    def thanh_toan(self):
        """Lưu thông tin thanh toán vào database và cập nhật trạng thái."""
        machitiet = self.txt_machitiet.text()
        madonban = self.txt_madonban_tt.text()
        matruyen = self.txt_matruyen.text()
        soluong = self.txt_soluong.value()

        try:
            dongia = float(self.txt_dongia.text())  # Chuyển đổi thành số thực
            thanhtien = soluong * dongia
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đúng định dạng số cho đơn giá.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO tbchitietdonban (machitiet, madonban, matruyen, soluong, dongia, thanhtien) VALUES (%s, %s, %s, %s, %s, %s)",
                (machitiet, madonban, matruyen, soluong, dongia, thanhtien)
            )
            self.cursor.execute(
                "UPDATE tbdonban SET tinhtrang = 'Đã thanh toán' WHERE madonban = %s", (madonban,)
            )
            self.conn.commit()
            self.load_data_table()  # Cập nhật dữ liệu trên tableWidget
            self.form_thanh_toan.close()
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi thanh toán: {err}")
    

    def show_chi_tiet_don_ban(self):
        """Hiển thị form xem chi tiết khi chọn một đơn bán."""
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một đơn bán để xem chi tiết.")
            return

        madonban = self.tableWidget.item(selected_row, 0).text()

        self.form_chi_tiet = QtWidgets.QDialog(self)
        self.form_chi_tiet.setWindowTitle("Chi Tiết Đơn Bán")

        layout = QtWidgets.QVBoxLayout()
        self.table_chi_tiet = QtWidgets.QTableWidget(self)
        self.table_chi_tiet.setColumnCount(6)
        self.table_chi_tiet.setHorizontalHeaderLabels(["Mã CT", "Mã Đơn", "Mã Truyện", "Số Lượng", "Đơn Giá", "Thành Tiền"])

        layout.addWidget(self.table_chi_tiet)
        self.load_chi_tiet_don_ban(madonban)

        btn_dong = QtWidgets.QPushButton("Đóng", self)
        btn_dong.clicked.connect(self.form_chi_tiet.close)
        layout.addWidget(btn_dong)

        self.form_chi_tiet.setLayout(layout)
        self.form_chi_tiet.exec()

    def load_chi_tiet_don_ban(self, madonban):
        """Lấy dữ liệu từ database và hiển thị trên bảng chi tiết."""
        try:
            self.cursor.execute(
                "SELECT machitiet, madonban, matruyen, soluong, dongia, thanhtien FROM tbchitietdonban WHERE madonban = %s",
                (madonban,)
            )
            data = self.cursor.fetchall()
            self.table_chi_tiet.setRowCount(len(data))
        
            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    self.table_chi_tiet.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {err}")
    
    def show_sua_don_ban(self):
        """Mở form sửa đơn bán khi chọn một đơn."""
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một đơn bán để sửa.")
            return

        self.madonban_sua = self.tableWidget.item(selected_row, 0).text()
        tenkhach = self.tableWidget.item(selected_row, 1).text()
        ngayban = self.tableWidget.item(selected_row, 2).text()

        self.form_sua_don = QtWidgets.QDialog(self)
        self.form_sua_don.setWindowTitle("Sửa Đơn Bán")

        layout = QtWidgets.QVBoxLayout()
        self.txt_madonban_sua = QtWidgets.QLineEdit(self)
        self.txt_madonban_sua.setText(self.madonban_sua)
        self.txt_madonban_sua.setReadOnly(True)

        self.txt_makhach_sua = QtWidgets.QLineEdit(self)
        self.txt_ngayban_sua = QtWidgets.QDateEdit(self)
        self.txt_ngayban_sua.setCalendarPopup(True)
        self.txt_ngayban_sua.setDate(QtCore.QDate.fromString(ngayban, "yyyy-MM-dd"))

        btn_luu = QtWidgets.QPushButton("Lưu", self)
        btn_luu.clicked.connect(self.sua_don_ban)

        layout.addWidget(QtWidgets.QLabel("Mã đơn bán:"))
        layout.addWidget(self.txt_madonban_sua)
        layout.addWidget(QtWidgets.QLabel("Mã khách mới:"))
        layout.addWidget(self.txt_makhach_sua)
        layout.addWidget(QtWidgets.QLabel("Ngày bán mới:"))
        layout.addWidget(self.txt_ngayban_sua)
        layout.addWidget(btn_luu)

        self.form_sua_don.setLayout(layout)
        self.form_sua_don.exec()

    def sua_don_ban(self):
        """Cập nhật thông tin đơn bán trong database."""
        madonban = self.madonban_sua
        makhach = self.txt_makhach_sua.text()
        ngayban = self.txt_ngayban_sua.date().toString("yyyy-MM-dd")

        if not makhach:
           QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mã khách.")
           return

        try:
            self.cursor.execute(
                "UPDATE tbdonban SET makhach = %s, ngayban = %s WHERE madonban = %s",
                (makhach, ngayban, madonban)
            )
            self.conn.commit()
            QtWidgets.QMessageBox.information(self, "Thành công", "Cập nhật đơn bán thành công!")

            self.load_data_table()  # Cập nhật lại tableWidget
            self.form_sua_don.close()
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi sửa đơn bán: {err}")
    
    def xoa_don_ban(self):
        try:
            # Lấy đơn thuê đang được chọn trên tableWidget
            selected_row = self.tableWidget.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đơn bán để xóa.")
                return       
            madonban = self.tableWidget.item(selected_row, 0).text()  # Cột 0 là mã đơn thuê       
            # Hỏi xác nhận trước khi xóa
            reply = QMessageBox.question(self, "Xác nhận xóa", "Bạn có chắc chắn muốn xóa đơn thuê này?",
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                             QMessageBox.StandardButton.No) 
            if reply == QMessageBox.StandardButton.No:
                return  # Không xóa nếu người dùng chọn "No"
            # Kiểm tra kết nối trước khi thực hiện truy vấn
            if not self.conn.is_connected():
                self.conn()  # Kết nối lại nếu bị mất
            # Xóa đơn thuê khỏi database
            self.cursor.execute("DELETE FROM tbdonban WHERE madonban = %s", (madonban,))
            self.conn.commit()
            # Xóa dòng trên tableWidget
            self.tableWidget.removeRow(selected_row)
            QMessageBox.information(self, "Thành công", "Đã xóa đơn bán thành công!")   
        except Exception as e:
            QMessageBox.critical(self, "Lỗi khi xóa đơn bán", str(e))
    
    def tim_kiem_don_ban(self):
        """Tìm kiếm đơn bán theo mã đơn, tên khách hoặc ngày bán."""
        keyword = self.lineEditBanTruyen.text().strip()  # Lấy dữ liệu từ lineEditBanTruyen

        if not keyword:
           self.load_data_table()  # Nếu không nhập gì thì load lại toàn bộ danh sách
           return

        try:
            query = """
            SELECT tbdonban.madonban, tbkhachhang.tenkhach, tbdonban.ngayban, tbdonban.tinhtrang 
            FROM tbdonban 
            INNER JOIN tbkhachhang ON tbdonban.makhach = tbkhachhang.makhach
            WHERE tbdonban.madonban LIKE %s 
            OR tbkhachhang.tenkhach LIKE %s 
            """
            self.cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
            rows = self.cursor.fetchall()

            # Hiển thị kết quả lên tableWidget
            self.tableWidget.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col_data)))
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi tìm kiếm: {err}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QLBT()
    window.show()
    sys.exit(app.exec())
