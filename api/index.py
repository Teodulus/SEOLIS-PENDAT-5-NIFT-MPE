# Simpan sebagai: api/index.py
# (Dengan path yang sudah FINAL dan BENAR)

from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handler(path):
    
    try:
        # --- PERBAIKAN FINAL DI SINI ---
        # KITA KEMBALIKAN KE VERSI ASLI (YANG SUDAH BENAR)
        
        # Path ke file python ini (misal: /var/task/api/index.py)
        current_file_path = os.path.abspath(__file__)
        # Path ke folder tempat file ini berada (misal: /var/task/api)
        current_dir = os.path.dirname(current_file_path)
        
        # PERGI SATU LEVEL KE ATAS (ke /var/task)
        parent_dir = os.path.dirname(current_dir)
        
        # Path ke CSV sekarang sudah benar
        csv_path = os.path.join(parent_dir, 'student_education_dataset.csv')
        # --- AKHIR PERBAIKAN FINAL ---

        if not os.path.exists(csv_path):
            # Pesan error jika masih tidak ditemukan
            return jsonify({"error": f"File CSV tidak ditemukan di path: {csv_path}. Path file script: {current_file_path}"}), 404
        
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
