import json
import os
from dotenv import load_dotenv
from google import genai
from CodeBlogUploader import buat_postingan

# Load environment variables sekali saja di tingkat modul
load_dotenv()

def generate_and_upload_blog(target_url="https://rs-bhayangkarasurabaya.id/"):
    """
    Fungsi untuk melakukan generate konten menggunakan Gemini 
    dan langsung mengunggahnya ke Blogger.
    """
    api_key = os.getenv("api_key")
    blog_id = os.getenv("blog_id")
    
    if not api_key or not blog_id:
        return {"status": "error", "message": "API Key atau Blog ID tidak ditemukan di .env"}

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Tugas: Analisis konten dari URL atau konteks judul berikut: {target_url} dan buatlah artikel blog yang SEO Friendly, unik, dan terdengar seperti ditulis manusia.

    INPUT:
    - Artikel asli: <article>{{11.`0`}}</article>

    INSTRUKSI PENULISAN:

    1. Gaya Penulisan:
    - Gunakan bahasa sederhana, santai, dan mudah dipahami semua orang.
    - Hindari istilah teknis yang rumit atau jargon berlebihan.
    - Gunakan gaya percakapan natural seperti blog umum.
    - Pecah paragraf panjang menjadi 2–4 kalimat.
    - Variasikan panjang kalimat agar lebih manusiawi.

    2. SEO Optimization:
    - Temukan keyword utama dari artikel dan gunakan secara natural.
    - Masukkan keyword di paragraf pembuka (lead paragraph).
    - Gunakan kata kunci turunan (LSI keyword) jika relevan.
    - Gunakan struktur heading jelas (H1, H2, H3).

    3. Humanisasi Konten:
    - Gunakan transisi antar paragraf agar mengalir.
    - Tambahkan analogi sederhana jika diperlukan.
    - Gunakan pertanyaan retoris untuk engagement.
    - Tambahkan contoh atau ilustrasi ringan jika relevan.

    4. Formatting HTML:
    - <h1> untuk judul utama
    - <h2> dan <h3> untuk subjudul
    - <p> untuk paragraf
    - <b> untuk penekanan penting
    - <ul> dan <li> untuk bullet points

    5. Judul Artikel (SANGAT PENTING):
    - Buat judul baru, bukan menyalin judul asli.
    - Judul harus SEO-friendly dan mengandung keyword utama.
    - Judul harus memiliki HOOK yang kuat untuk menarik klik.
    - Gunakan salah satu atau kombinasi:
        • curiosity gap (membangkitkan rasa penasaran)
        • problem–solution (menyelesaikan masalah)
        • benefit-driven (menunjukkan manfaat langsung)
        • angka/listicle jika relevan
    - Judul harus tetap natural, tidak clickbait berlebihan.

    Contoh gaya:
    - "Cara ... yang Jarang Diketahui Tapi Sangat Efektif"
    - "Mengapa ... Penting? Ini Fakta yang Sering Diabaikan"
    - "Panduan Lengkap ... untuk Pemula (Agar Tidak Salah Langkah)"
    - "5 Hal Penting tentang ... yang Wajib Kamu Tahu"

    6. Informasi Perusahaan & Lokasi Acara (PT Surya Sarana Dinamika):*
    - Anda WAJIB menyebutkan "PT Surya Sarana Dinamika" secara natural di dalam konten.
    - Identifikasi lokasi acara/topik dalam artikel yang diberikan untuk menyertakan informasi kontak dan alamat yang sesuai di akhir posting blog:
    - *Jika acara berlokasi di area Cikarang*, gunakan blok alamat berikut secara persis:
        PT Surya Sarana Dinamika - House of Industry 4.0
        Delta Commercial Park 1 Blok A No. 6
        Jl. Kenari Raya Delta Silicon 6
        Lippo Cikarang - Bekasi, 17530, Indonesia
        p: 0877 7041 1017
        e: [info@suryasarana.com](mailto:info@suryasarana.com)
        w: [www.suryasarana.com](http://www.suryasarana.com)
    - *Jika acara berlokasi di Jakarta (Sunter)*, gunakan blok alamat berikut secara persis:
        PT Surya Sarana Dinamika - Head Office
        Perkantoran Mega Sunter B-40
        Jl. Danau Sunter Selatan
        Jakarta, 14350, Indonesia
        p: 0877 7041 1017
        e: [info@suryasarana.com](mailto:info@suryasarana.com)
        w: [www.suryasarana.com](http://www.suryasarana.com)

    7. Panjang Artikel:
    - Minimal ±1000 kata.
    - Harus informatif, mendalam, dan enak dibaca.

    OUTPUT:
    Harus berupa JSON murni dengan format berikut:

    {{
        "kind": "blogger#post",
        "blog": {{ "id": "{blog_id}" }},
        "title": "Judul SEO Friendly dengan Hook Kuat",
        "content": "Isi artikel HTML lengkap (h1, h2, h3, p, b, ul, li)"
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        data = json.loads(response.text)
        
        hasil_upload = buat_postingan(data)

        if hasil_upload["status"] == "success":
            return {"status": "success", "data": data, "upload_response": hasil_upload}
        else:
            return {"status": "error", "data": data, "upload_response": hasil_upload}

    except json.JSONDecodeError as je:
        error_msg = f"Gagal parsing JSON. Raw: {response.text[:100]}..."
        print(error_msg)
        return {"status": "error", "message": error_msg}
    except Exception as e:
        error_msg = f"Terjadi kesalahan: {str(e)}"
        print(error_msg)
        return {"status": "error", "message": error_msg}

if __name__ == "__main__":
    generate_and_upload_blog("https://rs-bhayangkarasurabaya.id/")