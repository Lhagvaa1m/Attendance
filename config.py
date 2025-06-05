import os

creds_json = os.environ.get("GOOGLE_CREDS_JSON")
if creds_json:
    with open("credentials.json", "w") as f:
        f.write(creds_json)


API_TOKEN = os.environ.get("API_TOKEN")
CREDS_FILE = os.environ.get("CREDS_FILE", "credentials.json")
SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
SHEET_URL_EMPLOYEES = os.environ.get("SHEET_URL_EMPLOYEES")
SHEET_URL_ATTENDANCE = os.environ.get("SHEET_URL_ATTENDANCE")
SHEET_URL_LOCATION = os.environ.get("SHEET_URL_LOCATION")
WORKSHEET_NAME = os.environ.get("WORKSHEET_NAME", "offices")

print("API_TOKEN:", repr(API_TOKEN))
