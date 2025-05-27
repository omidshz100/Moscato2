import gspread
from google.oauth2.service_account import Credentials

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("Files/swift-atom-452517-m2-6029accc8a65.json", scopes=scope)
client = gspread.authorize(creds)

# Open the sheets by name or URL
sheet1 = client.open('Data-H').sheet1
sheet2 = client.open('Data-A').sheet1
sheet3 = client.open('All-data').sheet1

# Get all rows (as lists)
rows1 = sheet1.get_all_values()
rows2 = sheet2.get_all_values()
rows3 = sheet3.get_all_values()

# Convert rows to sets of tuples for comparison
set1 = set(tuple(row) for row in rows1)
set2 = set(tuple(row) for row in rows2)
set3 = set(tuple(row) for row in rows3)

# Check if all rows from sheet 1 and 2 exist in sheet 3
missing_from_3 = (set1 | set2) - set3

if missing_from_3:
    print("Rows missing from sheet 3:")
    print(len(missing_from_3), "rows are missing.")
else:
    print("All rows from sheet 1 and 2 exist in sheet 3.")