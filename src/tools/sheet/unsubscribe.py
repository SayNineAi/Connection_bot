from typing import Union
import gspread
import pandas as pd


def get_unsubscribe_sheet(
    acc: gspread.client.Client, sheet_url: Union[str, None]
) -> list:
    try:
        sheet = acc.open_by_url(sheet_url)
        uns_sheet = sheet.worksheet("Unsubscribe List")
        data = pd.DataFrame(uns_sheet.get_all_records())
        return data['LinkedIn URL'].to_list()
    except Exception as e:
        print(f"Error while getting unsubscribe sheet:\n {e}")
        return []
