import gspread
import pandas as pd

gc = gspread.service_account(filename='credentials-spread.json')
sh = gc.open_by_key("1RQEM7-IUGBdVu1aImZt_rg-CnM8iulCq3TMKrEL7Lt4")

worksheet = sh.sheet1 

header = ["Judul Postingan", "Kategori", "Status", "Tanggal"]
row1 = ["Cara Optimasi API", "Tutorial", "Draft", "2026-04-29"]
row2 = ["Update Google Sheets", "Berita", "Published", "2026-04-30"]
data_to_upload = [header, row1, row2]

worksheet.update('A1', data_to_upload)

data = worksheet.get_all_records()

df = pd.DataFrame(data)
print("Isi Spreadsheet Sekarang:")
print(df)