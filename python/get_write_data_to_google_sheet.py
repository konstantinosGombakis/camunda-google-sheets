import gspread
import json

with open('./cretential.json') as f:
    credentials = json.load(f)
    
gc = gspread.service_account_from_dict(credentials)

sh = gc.open_by_key("1jFHlcij79eiLlDhu2serhcn3ySSxmFrHb2bTYGpvHZg")
# sh = gc.open("mpms-google-sheet")


worksheet = sh.sheet1
cell='B2'
print(worksheet.acell(cell).value)

worksheet.update_acell(cell,48)
print(worksheet.acell(cell).value)
