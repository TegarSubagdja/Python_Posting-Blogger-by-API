# Blogger API Automation with Python

Script ini digunakan untuk memposting konten ke Blogger secara otomatis menggunakan Google Blogger API v3.

## 🚀 Persiapan Kredensial Google Cloud

Untuk menjalankan script ini, Anda memerlukan file kredensial `client_secrets.json`. Ikuti langkah-langkah berikut untuk mendapatkannya:

### 1. Setup Google Cloud Console
1. Buka [Google Cloud Console](https://console.cloud.google.com/).
2. Buat proyek baru melalui menu dropdown di pojok kiri atas > **New Project**.
3. Di bilah pencarian, cari **"Blogger API v3"**, klik hasilnya, lalu pilih **Enable**.

### 2. Konfigurasi OAuth Consent Screen
*Langkah ini wajib untuk menentukan siapa yang bisa mengakses aplikasi.*
1. Buka menu **APIs & Services > OAuth consent screen**.
2. Pilih User Type **External**, lalu klik **Create**.
3. Isi informasi wajib:
   - **App name**: (Contoh: "Blogger Automation Script")
   - **User support email**: (Email Anda)
   - **Developer contact info**: (Email Anda)
4. Klik **Save and Continue** sampai selesai (lewati bagian Scopes dan Test Users).
5. **Penting:** Setelah kembali ke dashboard OAuth Consent Screen, klik **Publish App** agar statusnya menjadi "In Production" (ini mencegah token kedaluwarsa dalam 7 hari).

### 3. Membuat & Mengunduh JSON
1. Buka menu **APIs & Services > Credentials**.
2. Klik **+ Create Credentials** > **OAuth client ID**.
3. Pilih Application type: **Desktop App**.
4. Beri nama (contoh: "Python Desktop Client"), lalu klik **Create**.
5. Pada daftar **OAuth 2.0 Client IDs**, temukan kredensial yang baru dibuat.
6. Klik ikon **Download** (panah bawah) di ujung kanan baris tersebut.
7. **Simpan file tersebut ke folder proyek Anda dan ubah namanya menjadi `client_secrets.json`.**

---

## 🛠️ Instalasi & Penggunaan

### 1. Install Dependencies
Pastikan Anda sudah menginstal library yang dibutuhkan:
```bash
pip install google-api-python-client google-auth-oauthlib
pip install beautifulsoup4 requests"# Python_Posting-Blogger-by-API" 
"# Python_Posting-Blogger-by-API" 
"# Python_Posting-Blogger-by-API" 
