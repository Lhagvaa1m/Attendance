# ==== sheets/base.py ====
# Google Sheets API ашиглан sheet-үүдтэй холбогддог үндсэн функц
from utils.gsheet_cache import (
    get_all_records,
    get_sheet as cached_get_sheet,
    get_worksheet,
)

def get_sheet(url):
    return cached_get_sheet(url)

# Google Sheets-ээс оффисуудын мэдээлэл авах utility функц энд байна.

def get_offices_from_sheet(sheet_url, creds_file='credentials.json', worksheet_name="offices"):
    worksheet = get_worksheet(sheet_url, worksheet_name)
    data = get_all_records(worksheet)
    offices = []
    for row in data:
        try:
            if not row['lat'] or not row['lon']:
                continue
            offices.append({
                'name': row['name'],
                'lat': float(row['lat']),
                'lon': float(row['lon'])
            })
        except Exception as e:
            print(f"Алдаатай мөр алгасав: {row} ({e})")
    return offices
