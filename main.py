import os
import re
import time
import gspread
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
from markdownify import markdownify as md
from CodeGeminiResume import generateContentBlog
from CodeBlogUploader import uploadContentBlog

load_dotenv()

def getDataSpreadsheet():
    try:
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error getting data from spreadsheet: {e}")
        return pd.DataFrame()

def updateDataSpreadsheet(df):
   try:
        header = df.columns.tolist()
        values = df.values.tolist()
        data_to_upload = [header] + values
        worksheet.update(range_name='A1', values=data_to_upload) 
        return "success"
   except Exception as e:
        print(f"Error updating data to spreadsheet: {e}")
        return "error"

def getContentUrl(url):
    try:
        content = requests.get(url)
        soup = bs(content.text, 'html.parser')
        markdown = md(str(soup))
        markdown = re.sub(r'[ \t]+', ' ', markdown)
        markdown = re.sub(r'\n\s*\n+', '\n', markdown)
        markdown = markdown.strip()
        return markdown
    except Exception as e:
        print(f"Error getting content from URL: {e}")
        return ""
    
gc = gspread.service_account(filename='credentials-spread.json')
sh = gc.open_by_key(os.getenv("spread_sheet_key"))
worksheet = sh.sheet1
df = getDataSpreadsheet()

for i in df.index:
    if not df.at[i, 'Status Blog'] == 'Success':

        url = df.at[i, 'Link']
        print(f"Memulai penarikan data dari URL {url}")
        content = getContentUrl(url)
        print(f"Data berhasil ditarik dari URL {url}")
        
        print(f"Memulai pembuatan konten blog")
        generateStatus = generateContentBlog(content, url)
        print(f"Konten blog berhasil dibuat")
        
        print(f"Memulai upload konten blog")
        uploadStatus = uploadContentBlog(generateStatus['message'])
        print(f"Konten blog berhasil diupload")

        if uploadStatus['status'] == 'success':
            df.at[i, 'Status Blog'] = 'Success'
            df.at[i, 'Date'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            print("success")
        else:
            df.at[i, 'Status Blog'] = 'Error'
            df.at[i, 'Date'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            print("error")
            
    time.sleep(3)

statusUpdate = updateDataSpreadsheet(df)

while True:
    pilihan = input("\nKeluar program? (y/n): ").strip().lower()
    if pilihan == 'y':
        break
    elif pilihan == 'n':
        print("Program tetap berjalan...")
    else:
        print("Input tidak valid. Ketik y atau n.")