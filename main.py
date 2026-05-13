import os
import re
import time
import json
import gspread
import requests
import pandas as pd
import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
from markdownify import markdownify as md
from CodeGeminiResume import generateContentBlog
from CodeBlogUpload import uploadContentBlog
from CodeGetStatitic import getSerankingPosition, calculateWeight

load_dotenv()

def getDataSpreadsheet():
    try:
        gc = gspread.service_account(filename='credentials-spread.json')
        sh = gc.open_by_key(os.getenv("spread_sheet_key"))
        worksheet = sh.sheet1
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
    
# Block Step by Step
with open ('Z_State.json', 'r') as f:
    state = json.load(f)

lastUpdate = datetime.datetime.strptime(state['last_update'], '%Y-%m-%d').date()

if datetime.date.today() <= lastUpdate:
    print("Belum waktunya untuk update.")
    print("Menghentikan program!")
    exit()

position = getSerankingPosition().json()[0]

listKeyword = []
for k in position['keywords']:
    weight = [n['pos'] - n['change'] for n in k['positions']]
    listKeyword.append([k['name'], sum(weight)])

listKeyword.sort(key=lambda x: x[1])
for l in listKeyword:
    print(l)

print(len(listKeyword))


    
