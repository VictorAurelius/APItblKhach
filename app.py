from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Cấu hình kết nối MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="api_kh"
)
cursor = db.cursor(dictionary=True)

# API: Lấy tất cả khách hàng
@app.route('/tblKhach', methods=['GET'])
def get_tblKhach():
    cursor.execute("SELECT * FROM tblKhach")
    tblKhach = cursor.fetchall()
    return jsonify(tblKhach)

# API: Lấy thông tin khách hàng theo MaKhach
@app.route('/tblKhach/<int:MaKhach>', methods=['GET'])
def get_customer(MaKhach):
    cursor.execute("SELECT * FROM tblKhach WHERE MaKhach = %s", (MaKhach,))
    customer = cursor.fetchone()
    return jsonify(customer) if customer else ('Not Found', 404)

# API: Xóa khách hàng
@app.route('/tblKhach/<int:MaKhach>', methods=['DELETE'])
def delete_customer(MaKhach):
    cursor.execute("DELETE FROM tblKhach WHERE MaKhach = %s", (MaKhach,))
    db.commit()
    return jsonify({"message": "Deleted successfully"}) if cursor.rowcount else ('Not Found', 404)

# API: Sửa thông tin khách hàng
@app.route('/tblKhach/<int:MaKhach>', methods=['PUT'])
def update_customer(MaKhach):
    data = request.json
    cursor.execute("UPDATE tblKhach SET TenKhach=%s, DiaChi=%s , DienThoai =%s WHERE MaKhach=%s", (data['TenKhach'], data['DiaChi'], data['DienThoai'], MaKhach))
    db.commit()
    return jsonify({"message": "Updated successfully"}) if cursor.rowcount else ('Not Found', 404)


@app.route('/tblKhach', methods=['POST'])
def add_customer():
    data = request.json
    try:
        # Kiểm tra số điện thoại đã tồn tại chưa
        cursor.execute("SELECT * FROM tblKhach WHERE DienThoai = %s", (data['DienThoai'],))
        if cursor.fetchone():
            return jsonify({"error": "Số điện thoại đã tồn tại"}), 400

        # Nếu chưa tồn tại, thực hiện thêm mới
        cursor.execute("INSERT INTO tblKhach (TenKhach, DiaChi, DienThoai) VALUES (%s, %s, %s)",
                       (data['TenKhach'], data['DiaChi'], data['DienThoai']))
        db.commit()
        return jsonify({"MaKhach": cursor.lastrowid, "message": "Customer added"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


if __name__ == '__main__':
    app.run(debug=True)