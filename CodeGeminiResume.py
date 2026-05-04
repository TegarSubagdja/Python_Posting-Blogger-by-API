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
    Tugas: Analisis konten dari URL berikut: {target_url} dan buatlah artikel blog yang SEO Friendly.
    
    Instruksi Konten & SEO:
    1. **Struktur**: Gunakan format HTML. Judul utama sebagai H1, bagi konten ke dalam beberapa sub-judul (H2 dan H3).
    2. **Kualitas**: Minimal 1000 karakter. Konten harus mendalam, informatif, dan relevan dengan isi link.
    3. **SEO**: 
       - Identifikasi kata kunci utama dari link tersebut dan gunakan secara natural di dalam teks.
       - Buatlah paragraf pembuka yang menarik (lead) yang mengandung kata kunci utama.
       - Gunakan bullet points (<ul> atau <ol>) untuk meningkatkan keterbacaan (readability).
       - Tambahkan teks tebal (<strong>) pada poin-poin penting.
    4. **Gaya Bahasa**: Profesional namun tetap menarik bagi pembaca umum.

    Output HARUS berupa JSON murni dengan struktur:
    {{
      "kind": "blogger#post",
      "blog": {{ "id": "{blog_id}" }},
      "title": "Judul Postingan SEO Friendly",
      "content": "Isi konten HTML lengkap dengan H2, H3, p, ul, dan strong (min 1000 karakter)"
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
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