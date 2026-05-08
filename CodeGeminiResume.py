import json
import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

def generateContentBlog(content, target_url):
    
    api_key = os.getenv("api_key")
    blog_id = os.getenv("blog_id")
    
    if not api_key or not blog_id:
        return {"status": "error", "message": "API Key atau Blog ID tidak ditemukan di .env"}

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Tugas: Analisis konten dari URL: {target_url} dan buatlah artikel blog 
    SEO Friendly, original, dan terdengar manusiawi dengan proper attribution.

    INPUT:
    - Content dari {target_url} adalah: {content}

    INSTRUKSI PENULISAN:

    1. ORIGINALITAS & CITATION:
    - Artikel HARUS original dengan perspektif unik, bukan sekadar rewrite.
    - Jika mengambil data/statistik spesifik, SELALU sertakan attribution.
    - Gunakan format: "Menurut [Sumber], ..." atau "Data dari [Sumber] menunjukkan..."
    - Paraphrase penuh tanpa copy-paste kalimat asli.
    - Tambahkan analisis/insight baru yang tidak ada di sumber asli.

    2. GAYA PENULISAN:
    - Bahasa sederhana, santai, seperti percakapan teman.
    - Variasikan panjang kalimat (2-4 kalimat per paragraf).
    - Gunakan transisi natural antar paragraf.
    - Tambahkan analogi sederhana jika diperlukan.

    3. SEO OPTIMIZATION:
    - Keyword utama di paragraf pembuka dan heading.
    - Gunakan LSI keyword jika relevan.
    - Struktur: H1 → H2 → H3 dengan hirarki jelas.

    4. JUDUL ARTICLE (CRITICAL):
    - Buat judul baru, bukan copy dari asli.
    - SEO-friendly + hook kuat yang membangkitkan penasaran.
    - Contoh: "Cara [Topik] yang Jarang Diketahui Tapi Efektif"
    - Contoh: "5 Hal Penting [Topik] yang Wajib Kamu Tahu Sekarang"

    5. FORMATTING HTML:
    - <h1>, <h2>, <h3> untuk struktur heading
    - <p> untuk paragraf
    - <b> untuk penekanan
    - <a href="[URL]">[Teks]</a> untuk link ke sumber

    6. MENTION PT SURYA SARANA DINAMIKA:
        - Anda WAJIB menyebutkan "PT Surya Sarana Dinamika" secara natural di dalam konten.
        - Identifikasi lokasi acara/topik dalam artikel yang diberikan untuk menyertakan informasi kontak dan alamat yang sesuai di akhir posting blog:
        - *Jika acara berlokasi di area Cikarang*, gunakan blok alamat berikut secara persis:
            PT Surya Sarana Dinamika - House of Industry 4.0
            Delta Commercial Park 1 Blok A No. 6
            Jl. Kenari Raya Delta Silicon 6
            Lippo Cikarang - Bekasi, 17530, Indonesia
            p: 0877 7041 1017
            e: <a href="mailto:info@suryasarana.com">info@suryasarana.com</a>
            w: <a href="http://www.suryasarana.com">www.suryasarana.com</a>
        - *Jika acara berlokasi di Jakarta (Sunter)*, gunakan blok alamat berikut secara persis:
            PT Surya Sarana Dinamika - Head Office
            Perkantoran Mega Sunter B-40
            Jl. Danau Sunter Selatan
            Jakarta, 14350, Indonesia
            p: 0877 7041 1017
            e: <a href="mailto:info@suryasarana.com">info@suryasarana.com</a>
            w: <a href="http://www.suryasarana.com">www.suryasarana.com</a>

    7. ATTRIBUTION:
        - Jika mengambil data/statistik spesifik dari sumber, gunakan hyperlink dengan format:
            Contoh: "Menurut <a href="[URL_SUMBER]">[Nama Sumber]</a>, data menunjukkan bahwa..."
        - Paraphrase penuh tanpa copy-paste, hanya sertakan link ke sumber asli jika ada data konkret yang dikutip.

    8. PANJANG: Minimal ±1000 kata dengan konten mendalam dan informatif.

    OUTPUT (JSON):
    {{
        "kind": "blogger#post",
        "blog": {{ "id": "{blog_id}" }},
        "title": "Judul SEO dengan Hook Kuat",
        "content": "HTML lengkap dengan h1-h3, p, b, a href untuk citation"
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

        return {"status": "success", "message": data}

    except json.JSONDecodeError as je:
        error_msg = f"Gagal parsing JSON. Raw: {response.text[:100]}..."
        print(error_msg)
        return {"status": "error", "message": error_msg}
    except Exception as e:
        error_msg = f"Terjadi kesalahan: {str(e)}"
        print(error_msg)
        return {"status": "error", "message": error_msg}

if __name__ == "__main__":
    generateContentBlog(
        "THK adalah pioner dari pada teknologi linea actuators. THK Co., Ltd. adalah perusahaan multinasional Jepang yang didirikan pada tahun 1971 dan dikenal luas sebagai inovator global terkemuka dalam teknologi Motion Control. Perusahaan ini adalah pionir dalam pengembangan dan produksi Teknologi Gerak Linear (Linear Motion Technology), yang menjadi tulang punggung bagi mesin dan sistem otomasi presisi di seluruh dunia. Dengan rekam jejak lebih dari 50 tahun, THK telah menetapkan standar industri untuk presisi, keandalan, dan inovasi dalam komponen mekanik.", 
        "https://www.suryasarana.com/brands/thk"
    )