import gspread
import pandas as pd
from datetime import datetime
from CodeGeminiResume import generate_and_upload_blog
import time

gc = gspread.service_account(filename='credentials-spread.json')
sh = gc.open_by_key("102jENB2-gOpjMN5Y52UMw7NeVXJAl5vkXDLcGWYc7kw")

worksheet = sh.sheet1

data = worksheet.get_all_records()
df = pd.DataFrame(data)

for i in df.index:
    if not df.at[i, 'Status Blog'] == 'Success':
        status = generate_and_upload_blog(df.at[i, 'Link'])
        if status['status'] == 'success':
            df.at[i, 'Status Blog'] = 'Success'
            df.at[i, 'Date'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            print("success")
        else:
            df.at[i, 'Status Blog'] = 'Error'
            df.at[i, 'Date'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            print("error")
            
    time.sleep(3)
        
header = df.columns.tolist()
values = df.values.tolist()
data_to_upload = [header] + values  

worksheet.update(range_name='A1', values=data_to_upload)        
print(df)