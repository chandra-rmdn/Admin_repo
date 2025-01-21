import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from mysql.connector import Error

app = Flask(__name__)

def get_connection():
    try: 
        connection = mysql.connector.connect(
            host = "tlw44.h.filess.io",
            database = "DataProduk_mineralsis",
            port = "3307",
            user = "DataProduk_mineralsis",
            password = "66d5729d92ed1cad20b08d72d53e271810fc25b2"
        )
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

try:
    connection = get_connection()
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

def generate_kode_barang():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT kode_barang FROM data_barang ORDER BY kode_barang DESC LIMIT 1")
            result = cursor.fetchone()

            if result is None:  # Jika tidak ada data, mulai dari B-001
                return "B-001"
            else:
                last_kode = result[0]  # Ambil kode barang terakhir, misalnya "B-001"
                number = int(last_kode.split('-')[1]) + 1  # Pisahkan angka, tambah 1
                return f"B-{number:03d}"
        except Error as e:
            print("Error while deleting data:", e)
        finally:
            cursor.close()
            connection.close()

@app.route('/')
def index():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM data_barang")
        result = cursor.fetchall()
        cursor.close()
        connection.close()
    else:
        result = []
        print("Unable to connect to database")
    return render_template('index.html', hasil=result)

def total_qty():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT SUM(qty) AS total_qty FROM data_barang")
            result = cursor.fetchone()
            total_qty = result[0] if result[0] is not None else 0
        except Error as e:
            print("Error while deleting data:", e)
        finally:
            cursor.close()
            connection.close()
    return total_qty

@app.route('/data_stok/')
def data_stok():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM data_barang")
            result = cursor.fetchall()
            total_qty_value = total_qty()
        except Error as e:
            print("Error while deleting data:", e)
        finally:
            cursor.close()
            connection.close()
    return render_template('form_data_stok.html', hasil = result, total_qty = total_qty_value)
    
## Tambah ##    
@app.route('/tambah/')
def tambah_data():
    kode_barang = generate_kode_barang()
    return render_template('form_input.html', kode_barang = kode_barang)

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    kode_barang = request.form['kode_barang']
    nama_barang = request.form['nama_barang']
    type = request.form['type']
    unit = request.form['unit']
    harga_beli = request.form['harga_beli']
    harga_jual = request.form['harga_jual']
    qty = request.form['qty']
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO data_barang (kode_barang, nama_barang, type, unit, harga_beli, harga_jual, qty) VALUES (%s, %s, %s, %s, %s, %s, %s)", (kode_barang, nama_barang, type, unit, harga_beli, harga_jual, qty))
            connection.commit()
        except Error as e:
            print("Error while inserting data:", e)
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('index'))

## Ubah ##
@app.route('/ubah/<kode_barang>', methods=['GET'])
def ubah_data(kode_barang):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM data_barang WHERE kode_barang = %s", (kode_barang,))
            result = cursor.fetchall()
        except Error as e:
            print("Error while inserting data:", e)
        finally:
            cursor.close()
            connection.close()
    return render_template('form_ubah.html', hasil = result)

## Ubah Form Data Barang ##
@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    kode = request.form['kode_ori']
    kode_barang = request.form['kode_barang']
    nama_barang = request.form['nama_barang']
    type = request.form['type']
    unit = request.form['unit']
    harga_beli = request.form['harga_beli']
    harga_jual = request.form['harga_jual']
    qty = request.form['qty']
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            sql = 'UPDATE data_barang SET kode_barang=%s, nama_barang=%s, type=%s, unit=%s, harga_beli=%s, harga_jual=%s, qty=%s WHERE kode_barang=%s'
            value = (kode_barang, nama_barang, type, unit, harga_beli, harga_jual, qty, kode)
            cursor.execute(sql, value)
            connection.commit()
        except Error as e:
            print("Error while inserting data:", e)
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('index'))

@app.route('/hapus/<kode_barang>', methods=['GET'])
def hapus_data(kode_barang):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE from data_barang WHERE kode_barang=%s', (kode_barang,))
            connection.commit()
        except Error as e:
            print("Error while inserting data:", e)
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)