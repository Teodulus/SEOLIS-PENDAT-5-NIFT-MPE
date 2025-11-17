# Simpan sebagai: api/students.py

from flask import Flask, jsonify, request  # <-- 'request' penting untuk membaca ID
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handler(path):
    
    try:
        # 1. TEMUKAN & BACA CSV
        # Kode ini mencari file CSV yang ada di folder root (satu level di atas folder 'api')
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, 'student_education_dataset.csv')

        if not os.path.exists(csv_path):
            return jsonify({"error": "File CSV tidak ditemukan."}), 404
        
        # Pandas membaca seluruh CSV ke dalam memori
        df = pd.read_csv(csv_path)

        # 2. INI KONEKSINYA: Ambil ID dari JavaScript
        # JavaScript mengirim: /api/students?id=123
        # 'request.args.get('id')' akan mengambil "123"
        student_id_str = request.args.get('id')

        if student_id_str:
            # 3A. JIKA ADA ID: Cari satu siswa
            try:
                student_id = int(student_id_str) # Ubah "123" (teks) jadi 123 (angka)
            except ValueError:
                return jsonify({"error": "ID harus berupa angka."}), 400
            
            # Cari siswa di DataFrame Pandas
            student_data = df[df['StudentID'] == student_id]
            
            if student_data.empty:
                # Jika ID tidak ditemukan
                return jsonify({"error": f"Siswa dengan ID {student_id} tidak ditemukan."}), 404
            else:
                # Jika ditemukan, kirim datanya sebagai JSON
                result = student_data.iloc[0].to_dict()
                return jsonify(result) # Ini adalah "jawaban telepon" ke JavaScript

        else:
            # 3B. JIKA TIDAK ADA ID: Kembalikan semua data
            # (Fungsi ini tidak terpakai di frontend kita, tapi bagus untuk tes)
            data = df.to_dict(orient='records')
            return jsonify(data)

    except Exception as e:
        # Jika ada error di Python, kirim pesannya ke JavaScript
        return jsonify({"error": str(e)}), 500
