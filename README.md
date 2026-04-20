# Proyek Analisis Data: Brazilian E-Commerce (Olist) 🛒

## Deskripsi
Proyek ini bertujuan untuk menganalisis performa bisnis E-Commerce Olist selama periode 2017-2018. Fokus utama analisis meliputi identifikasi kategori produk unggulan, tren pertumbuhan pesanan bulanan, serta analisis perilaku pelanggan menggunakan metode RFM.

## Struktur Folder
- **dashboard/**: Berisi file `dashboard.py` dan dataset `main_data.csv` untuk visualisasi interaktif.
- **data/**: Berisi seluruh dataset mentah dalam format CSV.
- **notebook.ipynb**: File analisis data lengkap mulai dari Gathering hingga Visualisasi.
- **README.md**: Panduan penggunaan proyek.
- **requirements.txt**: Daftar library Python yang diperlukan.

## Cara Menjalankan Dashboard

### 1. Buka Folder Project
Pastikan terminal Anda berada di direktori utama proyek (folder `submission`).
```bash
cd submission

### 2. Buat Virtual Environment
python -m venv venv

### 3. Aktifkan Virtual Environment
Untuk Windows:
venv\Scripts\activate

Untuk Mac/Linux:
source venv/bin/activate

### 4. Install Library yang Dibutuhkan
Pasang semua dependensi dengan menjalankan perintah berikut:
pip install -r requirements.txt

### 5. Jalankan Notebook
Buka dan jalankan file notebook.ipynb dari awal hingga akhir untuk menghasilkan file dashboard/main_data.csv.

### 6. Jalankan Dashboard Streamlit
streamlit run dashboard/dashboard.py

### 7. Buka di Browser
Dashboard dapat diakses melalui: http://localhost:8501