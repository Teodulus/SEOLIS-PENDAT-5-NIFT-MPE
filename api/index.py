# Simpan sebagai: api/index.py
# (Versi FINAL dengan path os.getcwd())

from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handler(path):
    
    try:
        # --- PATH INI SUDAH BENAR ---
        # Di Vercel, os.getcwd() akan mengarah ke /var/task
        base_dir = os.getcwd()
        
        # Path ke CSV akan menjadi /var/task/student_education_dataset.csv
        csv_path = os.path.join(base_dir, 'student_education_dataset.csv')
        # --- AKHIR PATH ---

        if not os.path.exists(csv_path):
            # Pesan error yang lebih detail untuk debugging
            return jsonify({
                "error": "File CSV tidak ditemukan.",
                "cek_path_ini": csv_path,
                "base_dir": base_dir
            }), 404
        
        df = pd.read_csv(csv_path)

        # 2. Ambil ID dari JavaScript
        student_id_str = request.args.get('id')

        if student_id_str:
            # 3A. JIKA ADA ID: Cari satu siswa
            try:
                student_id = int(student_id_str)
            except ValueError:
                return jsonify({"error": "ID harus berupa angka."}), 400
            
            student_data = df[df['StudentID'] == student_id]
            
            if student_data.empty:
                return jsonify({"error": f"Siswa dengan ID {student_id} tidak ditemukan."}), 404
            else:
                result = student_data.iloc[0].to_dict()
                return jsonify(result)

        else:
            # 3B. JIKA TIDAK ADA ID: Kembalikan semua data
            data = df.to_dict(orient='records')
            return jsonify(data)

    except Exception as e:
        # Mengirim error sebagai JSON agar mudah di-debug
        return jsonify({"error": f"Terjadi kesalahan pada server: {str(e)}"}), 500
