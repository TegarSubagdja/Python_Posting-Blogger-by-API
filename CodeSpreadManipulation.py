import gspread
import pandas as pd
from datetime import datetime
from CodeGeminiResume import generate_and_upload_blog

gc = gspread.service_account(filename='credentials-spread.json')
sh = gc.open_by_key("1RQEM7-IUGBdVu1aImZt_rg-CnM8iulCq3TMKrEL7Lt4")

worksheet = sh.sheet1

data = worksheet.get_all_records()
df = pd.DataFrame(data)

for i in df.index:
    if not df.at[i, 'Status Blog'] == '':
        df.at[i, 'Status Blog'] = 'Process'
        df.at[i, 'Date'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        
header = df.columns.tolist()
values = df.values.tolist()
data_to_upload = [header] + values

worksheet.update('A1', data_to_upload)        
print(df)