QuranApp Backend

Aplikasi backend sederhana untuk QuranApp, dibangun menggunakan Python 3.11 dan Flask. Menyediakan berbagai endpoint untuk daftar surah, detail ayat, serta pencarian semantik.

Getting Started

- Clone repository:
  git clone https://github.com/defrindr/quranapp-backend.git
  cd quranapp-backend

- Buat dan aktifkan virtual environment:
  python3.11 -m venv venv
  source venv/bin/activate
  (di Windows: venv\Scripts\activate)

- Install dependencies:
  pip install -r requirements.txt

- Jalankan server:
  flask run

  (pastikan FLASK_APP sudah diset, jika belum jalankan:
   export FLASK_APP=app.py
   export FLASK_ENV=development
   )

- Akses API melalui:
  http://localhost:5000

Environment Variables

Buat file .env (opsional) jika menggunakan python-dotenv.

Contoh:
FLASK_APP=app.py
FLASK_ENV=development

Fitur

- Endpoint /surah_list untuk daftar surah
- Endpoint /surah_detail/<surah_number> untuk detail ayat per surah
- Endpoint /semantic_search untuk pencarian potongan ayat berdasarkan teks
- Menggunakan pandas dan data CSV untuk sumber data
- Dukungan CORS untuk akses dari frontend

Struktur Direktori

- app.py                    Entry point utama Flask app
- data/                     Folder penyimpanan CSV atau file data
- utils.py (opsional)       Fungsi bantu seperti pembacaan file atau pencarian

Dependencies

- Flask
- Flask-CORS
- pandas
- scikit-learn (jika digunakan untuk vectorizer pencarian semantik)
- python-dotenv (opsional)

Catatan

Pastikan semua data (misalnya file CSV) tersedia di folder yang sesuai.
Jika menggunakan semantic search berbasis vektor, pastikan library seperti scikit-learn dan dependensi vectorizer sudah terinstal.
