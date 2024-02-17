from src.model.connection import ConnectLinkedin
from config import *


if __name__ == "__main__":
    connect = ConnectLinkedin(
        input_json=INPUT_JSON,
        input_sheet=SHEET_URL,
        login=LOGIN,
        password=PASSWORD,
        driver=DRIVER_DIR,
        profile=PROFILE_NAME,
        user_data_dir=USER_DIR_PATH
    )
    connect.start()
