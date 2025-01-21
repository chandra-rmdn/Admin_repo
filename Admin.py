from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from mysql import connector

app = Flask(__name__)

db = connector.connect(
    host ="localhost",
    user = "root",
    password = "",
    database = "db_barang"
)

if db.is_connected():
    print("MySQL Connected")

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_barang")
    result = cursor.fetchall()
    cursor.close()
    return render_template('index.html', hasil = result)

def total_qty():
    cursor = db.cursor()
    cursor.execute("SELECT SUM(qty) AS total_qty FROM data_barang")
    result = cursor.fetchone()
    total_qty = result[0] if result[0] is not None else 0
    cursor.close()
    return total_qty

@app.route('/data_stok/')
def data_stok():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_barang")
    result = cursor.fetchall()
    total_qty_value = total_qty()
    cursor.close()
    return render_template('form_data_stok.html', hasil = result, total_qty = total_qty_value)

def generate_kode_barang():
    cursor = db.cursor()
    cursor.execute("SELECT kode_barang FROM data_barang ORDER BY kode_barang DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()

    if result is None:  # Jika tidak ada data, mulai dari B-001
        return "B-001"
    else:
        last_kode = result[0]  # Ambil kode barang terakhir, misalnya "B-001"
        number = int(last_kode.split('-')[1]) + 1  # Pisahkan angka, tambah 1
        return f"B-{number:03d}"
    
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
    cursor = db.cursor()
    cursor.execute("INSERT INTO data_barang (kode_barang, nama_barang, type, unit, harga_beli, harga_jual, qty) VALUES (%s, %s, %s, %s, %s, %s, %s)", (kode_barang, nama_barang, type, unit, harga_beli, harga_jual, qty))
    db.commit()
    return redirect(url_for('index'))

## Ubah ##
@app.route('/ubah/<kode_barang>', methods=['GET'])
def ubah_data(kode_barang):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data_barang WHERE kode_barang = %s", (kode_barang,))
    result = cursor.fetchall()
    cursor.close()
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
    cursor = db.cursor()
    sql = 'UPDATE data_barang SET kode_barang=%s, nama_barang=%s, type=%s, unit=%s, harga_beli=%s, harga_jual=%s, qty=%s WHERE kode_barang=%s'
    value = (kode_barang, nama_barang, type, unit, harga_beli, harga_jual, qty, kode)
    cursor.execute(sql, value)
    db.commit()
    return redirect(url_for('index'))

@app.route('/hapus/<kode_barang>', methods=['GET'])
def hapus_data(kode_barang):
    cursor = db.cursor()
    cursor.execute('DELETE from data_barang WHERE kode_barang=%s', (kode_barang,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)