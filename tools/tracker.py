import gspread
from datetime import date
import os

def date_to_serial(d):
    delta = d - date(1899, 12, 30)
    return delta.days # Google Date serial


def job_tracker(company_name:str, job_title:str):
    
    gc = gspread.service_account()
    
    sh = gc.open(os.getenv('GOOGLE_SHEET_NAME'))
    
    worksheet = sh.get_worksheet(0)
    worksheet.update_title('Applications')
    
    existing_header = worksheet.row_values(1)
    if not existing_header:
        # Append the header
        worksheet.append_row(['Date', 'Company', 'Job Title', 'Status', 'Notes'])
        
        # Format the header
        worksheet.format('A1:E1', {'textFormat' : {
            'fontSize': 16,
            'bold': True
        }})
        
        # Format the Date
        worksheet.format('A2:A1000', {'numberFormat': {
            'type': 'DATE',
            'pattern': 'dd/mm/yyyy'
        }})
        
    today_serial = date_to_serial(date.today())
    
    worksheet.append_row([today_serial, company_name, job_title, 'Applied', ''])
    
    return "New row has been added!"