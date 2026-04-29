import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

BLOG_ID = '121149020945595556' 
SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_blogger_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('blogger', 'v3', credentials=creds)

def buat_postingan(body):
    try:
        service = get_blogger_service()
        
        request = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=True)
        response = request.execute()

        print("---")
        print(f"Postingan Berhasil Dibuat!")
        print(f"Judul: {response['title']}")
        print(f"URL  : {response['url']}")
        print("---")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")