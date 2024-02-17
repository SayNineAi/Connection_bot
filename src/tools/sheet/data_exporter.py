import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def export_data_to_sheet(
    acc: gspread.client.Client,
    data_file_path: str,
    sheet_url: str,
    email: str,
    version: str,
):
    try:
        data = pd.read_csv(data_file_path)
        sheet = acc.open_by_url(sheet_url)
        new_worksheet_title = f"{email}_{version}"

        # Check if the worksheet already exists
        worksheets = sheet.worksheets()
        existing_worksheet = next(
            (ws for ws in worksheets if ws.title == new_worksheet_title), None
        )

        if existing_worksheet:
            # Append data to existing worksheet
            existing_data = pd.DataFrame(existing_worksheet.get_all_records())
            combined_data = pd.concat([existing_data, data], ignore_index=True)
            # Remove duplicates based on "linkedinUrl" column
            combined_data = combined_data.drop_duplicates(subset=["userUrl"])
            # Clear existing worksheet
            existing_worksheet.clear()
            # Write the combined data to the worksheet
            set_with_dataframe(existing_worksheet, combined_data)
        else:
            # Create a new worksheet
            new_worksheet = sheet.add_worksheet(
                title=new_worksheet_title, rows=data.shape[0], cols=data.shape[1]
            )
            # Write the DataFrame to the new worksheet
            set_with_dataframe(new_worksheet, data)

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


#
def connect_to_sheet(input_json) -> gspread.client.Client:
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(input_json, scopes)
    acc = gspread.authorize(credentials)
    return acc
