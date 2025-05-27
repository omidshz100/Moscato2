import gspread
from google.oauth2.service_account import Credentials
import requests
import time

# all the column names 

def connect_to_google_sheet(sheet_name, creds_json_path):
    """
    Connects to a Google Sheet using service account credentials.

    Args:
        sheet_name (str): The name of the Google Sheet to connect to.
        creds_json_path (str): Path to the service account JSON credentials file.

    Returns:
        gspread.Spreadsheet: The connected Google Sheet object.
    """
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(creds_json_path, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name)
    return sheet

# Function to add a row to the Google Sheet - dict to list conversion - template inside the function
def add_row_to_sheet(sheet, row_values: dict):
    """
    Adds a row to the first worksheet of the Google Sheet using the provided dictionary.
    The keys of row_values should match the column headers in the sheet.

    Args:
        sheet (gspread.Spreadsheet): The connected Google Sheet object.
        row_values (dict): Dictionary mapping column names to their values.

    Returns:
        dict: The API response from gspread's append_row.
    """
    worksheet = sheet.sheet1
    headers = worksheet.row_values(1)
    row_list = [row_values.get(header, '') for header in headers]
    return worksheet.append_row(row_list, value_input_option='USER_ENTERED')


def get_all_rows(sheet, column_names=None):
    """
    Retrieves all rows from the first worksheet of the Google Sheet, optionally mapping to specified column names.

    Args:
        sheet (gspread.Spreadsheet): The connected Google Sheet object.
        column_names (list, optional): List of column names to filter each row dict. If None, returns all columns.

    Returns:
        list: A list of dicts (if column_names provided) or lists (raw rows).
    """
    worksheet = sheet.sheet1
    rows = worksheet.get_all_values()
    if not rows:
        return []
    headers = rows[0]
    data_rows = rows[1:]
    dict_rows = [dict(zip(headers, row)) for row in data_rows]
    if column_names:
        # Only include specified columns in each dict
        filtered_rows = [{col: row.get(col, "") for col in column_names} for row in dict_rows]
        return filtered_rows
    return dict_rows

def update_row_in_sheet(sheet, search_column, search_value, update_dict):
    """
    Searches for a row where search_column == search_value and updates columns with values from update_dict.

    Args:
        sheet (gspread.Spreadsheet): The connected Google Sheet object.
        search_column (str): The column name to search for.
        search_value (str): The value to match in the search_column.
        update_dict (dict): Dictionary of column names and their new values.

    Returns:
        bool: True if a row was updated, False otherwise.
    """
    worksheet = sheet.sheet1
    headers = worksheet.row_values(1)
    try:
        col_idx = headers.index(search_column)
    except ValueError:
        return False

    all_rows = worksheet.get_all_values()
    for i, row in enumerate(all_rows[1:], start=2):  # start=2 because row 1 is headers
        if len(row) > col_idx and row[col_idx] == search_value:
            # Prepare updated row
            updated_row = list(row) + [''] * (len(headers) - len(row))
            for key, value in update_dict.items():
                if key in headers:
                    idx = headers.index(key)
                    updated_row[idx] = value
            # Ensure updated_row is exactly the same length as headers
            updated_row = updated_row[:len(headers)]
            # Use gspread.utils.rowcol_to_a1 for robust range (row, col)
            from gspread.utils import rowcol_to_a1
            start_cell = rowcol_to_a1(i, 1)
            end_cell = rowcol_to_a1(i, len(headers))
            worksheet.update(range_name=f"{start_cell}:{end_cell}", values=[updated_row])
            return True
    return False
def get_rows_by_column_value(sheet, column_name, value):
    """
    Retrieves all rows from the first worksheet where the specified column matches the given value.

    Args:
        sheet (gspread.Spreadsheet): The connected Google Sheet object.
        column_name (str): The column name to search.
        value (str): The value to match in the specified column.

    Returns:
        list: A list of dicts representing the matching rows.
    """
    worksheet = sheet.sheet1
    rows = worksheet.get_all_values()
    if not rows:
        return []
    headers = rows[0]
    try:
        col_idx = headers.index(column_name)
    except ValueError:
        return []
    data_rows = rows[1:]
    matching_rows = [
        dict(zip(headers, row))
        for row in data_rows
        if len(row) > col_idx and row[col_idx] == value
    ]
    return matching_rows

# propmpt for the function get_aifa_urls
'''
A function get input as AIC then return dictionary 

"pdf_url:"https://api.aifa.gov.it/aifa-bdf-eif-be/1.0.0/organizzazione/{codiceSis}/farmaci/{aic6}/stampati?ts=RCP"
"json_url":"https://api.aifa.gov.it/aifa-bdf-eif-be/1.0.0/formadosaggio/ricerca?query=0{aic}&spellingCorrection=true&page=0"
first get the codiceSis and aic6 from the json_url then : 
check if ["data"]["content"] is not null :  data["data"]["content"] then 
codiceSis = data["data"]["content"][0]["medicinale"]["codiceSis"]
ic6 = data["data"]["content"][0]["medicinale"]["aic6"]

return {
    "pdf_url": f"https://api.aifa.gov.it/aifa-bdf-eif-be/1.0.0/organizzazione/{codiceSis}/farmaci/{aic6}/stampati?ts=RCP",
    "json_url": f"https://api.aifa.gov.it/aifa-bdf-eif-be/1.0.0/formadosaggio/ricerca?query=0{aic6}&spellingCorrection=true&page=0"
}

if the ["data"]["content"] is null then return None
'''
def get_aifa_urls(aic):
    """
    Given an AIC code, fetches codiceSis and aic6 from the AIFA API and returns the PDF and JSON URLs.
    Returns None if the content is missing.
    """
    json_url = f"https://api.aifa.gov.it/aifa-bdf-eif-be/1.0.0/formadosaggio/ricerca?query=0{aic}&spellingCorrection=true&page=0"
    try:
        response = requests.get(json_url)
        response.raise_for_status()
        data = response.json()
        content = data.get("data", {}).get("content")
        if content and len(content) > 0:
            medicinale = content[0].get("medicinale", {})
            codiceSis = medicinale.get("codiceSis")
            aic6 = medicinale.get("aic6")
            # Check if codiceSis and aic6 are not None
            codiceAtc = content[0].get("codiceAtc")[0] if content[0].get("codiceAtc") else None
            descrizioneAtc = content[0].get("descrizioneAtc")[0] if content[0].get("descrizioneAtc") else None
            if codiceSis and aic6:
                return {
                    "URL_PDF": f"https://api.aifa.gov.it/aifa-bdf-eif-be/1.0.0/organizzazione/{codiceSis}/farmaci/{aic6}/stampati?ts=RCP",
                    "URL_json": f"https://api.aifa.gov.it/aifa-bdf-eif-be/1.0.0/formadosaggio/ricerca?query=0{aic}&spellingCorrection=true&page=0",
                    "ATC": f"{codiceAtc} - {descrizioneAtc}"
                }
    except Exception:
        pass
    return None

if __name__ == "__main__":
    # Example usage
    # sheet_name = "test"
    sheet_name = "All-data"  # Replace with the actual name of your Google Sheet.
    # Replace with the actual path to your downloaded Google service account credentials JSON file.
    # You can obtain this file from the Google Cloud Console after creating a service account and enabling the Google Sheets API.
    creds_json_path = "Files/swift-atom-452517-m2-6029accc8a65.json"
    
    try:
        sheet = connect_to_google_sheet(sheet_name, creds_json_path)
            # Example of adding a row to the sheet
        #     add_row_to_sheet(sheet, {
        #     'Principio Attivo': '1',
        #     'Descrizione Gruppo': '2',
        #     'Denominazione e Confezione': '3',
        #     'Titolare AIC': '4',
        #     'Codice  AIC': '5',
        #     'Codice Gruppo Equivalenza': '6',
        #     'Class': '7',
        #     '4.1 Indicazioni terapeutiche': '8',
        #     '4.2 Posologia e modo di somministrazione': '9',
        #     '4.3 Contraindications': '10',
        #     '4.4 Special warnings and precautions for use': '11',
        #     '4.5 Interactions with other medicinal products': '12',
        #     '4.6 Fertility, pregnancy and lactation': '13',
        #     '4.7 Effects on ability to drive and use machines': '14',
        #     '4.8 Undesirable effects (side effects)': '15',
        #     '4.9 Overdose': 'Overdose example',
        #     '6.2 Incompatibilities': '16',
        #     'CLASS': '17',
        #     'URL': '18',
        #     'URL_json': '19'
        # })
        
        # Example of retrieving all rows from the sheet
        # result = get_all_rows(sheet, column_names=[
        #     'Codice  AIC'
        # ])
        # for item in result:
            # print(item['Codice  AIC'])
        # Example of updating a row in the sheet
        # update_row_in_sheet(sheet, 'Codice  AIC', '5', {
        #     'Principio Attivo': "AAAAAAAAAA", 'Descrizione Gruppo': "A",
        #     'Denominazione e Confezione': "A", 'Titolare AIC': "A",
        #     'Codice  AIC': "5", 'Codice Gruppo Equivalenza': "A",
        #     'Class': "A", '4.1 Indicazioni terapeutiche': "A",
        #     '4.2 Posologia e modo di somministrazione': "A",
        #     '4.3 Contraindications': "A",
        #     '4.4 Special warnings and precautions for use': "A",
        #     '4.5 Interactions with other medicinal products': "A",
        #     '4.6 Fertility, pregnancy and lactation': "A",
        #     '4.7 Effects on ability to drive and use machines': "A",
        #     '4.8 Undesirable effects (side effects)': "A",
        #     '4.9 Overdose': "A",
        #     '6.2 Incompatibilities': "A",
        #     'CLASS': "A",
        #     'ATC': "A",
        #     'URL': "A",
        #     'URL_json': "A"
        # })
        # # Example of getting rows by column value
        # result = get_rows_by_column_value(sheet, 'Codice  AIC', '5')
        # print(result)
        
        
        result_all_AICs = get_all_rows(sheet, column_names=['Codice  AIC'])
        for item_aic in result_all_AICs[3171:3365]:  # Limit to first 10 for testing
            print(f"thread#2 - Processing AIC: {item_aic['Codice  AIC']}")
            update_data = get_aifa_urls(item_aic['Codice  AIC'])
            if update_data is not None:
                print(f"Updating AIC: {item_aic['Codice  AIC']} with data: {update_data}")
                update_row_in_sheet(sheet, 'Codice  AIC', str(item_aic['Codice  AIC']), {
                    'ATC': update_data['ATC'],  
                    'URL_PDF': update_data['URL_PDF'],
                    'URL_json': update_data['URL_json']
                })
                time.sleep(1)
            else:
                print(f"No data found for AIC: {item_aic}")
            time.sleep(2)
        
    except gspread.exceptions.SpreadsheetNotFound:
        print("The specified Google Sheet was not found.")
    except gspread.exceptions.APIError as api_error:
        print(f"API error occurred: {api_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

