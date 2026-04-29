import gspread
import pandas as pd

gc = gspread.service_account(filename='credentials-spread.json')
sh = gc.open_by_key("1RQEM7-IUGBdVu1aImZt_rg-CnM8iulCq3TMKrEL7Lt4")

worksheet = sh.sheet1
data = worksheet.get_all_records()

df = pd.DataFrame(data)
print(df)