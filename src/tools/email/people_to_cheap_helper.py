import os
import gspread
import pyautogui
import pandas as pd
from time import sleep
from random import randint
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials


#
def connect_to_sheet(input_json):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        input_json, scopes
    )
    acc = gspread.authorize(credentials)
    return acc


#
def send_data_to_sheet(acc, data, sheet_url):
    sheet = acc.open_by_url(sheet_url).sheet1
    sheet.clear()
    set_with_dataframe(sheet, data)
    return True


#
def export_data_to_sheet(acc, data, sheet_url):
    sheet = acc.open_by_url(sheet_url)
    sheet.clear()
    set_with_dataframe(sheet, data)
    return True


#
def find_position(email, dct):
    for key in dct:
        if email in dct[key]:
            return key, dct[key].index(email)
    return False, False


#
def favorite(df):
    # Not favorite if priority == min_value
    min_priority = df.groupby("original domain")["priority"].transform("min")
    df["favorite"] = [
        "Favorite" if priority == min_val and min_val < 5000 else "Not Favorite"
        for priority, min_val in zip(df["priority"], min_priority)
    ]
    return df


#
def post_data(df, header, output):
    df = favorite(df)
    df.to_csv(output, index=False, header=header, encoding="utf-8")


#
def process_data(df, mail_variations, finish_df, header, output):
    print("LEN OF DF", len(df.index))

    for _, row in df.iterrows():
        if row["result"] == "FALSE":
            email_value = row["email 2"].strip()
            row_index = row["index"]
            for i in range(1, 10):
                variant_column = f"email"
                if pd.isna(finish_df.loc[row_index, variant_column]):
                    finish_df.at[row_index, variant_column] = str(email_value)
                    break

    post_data(finish_df, header=header, output=output)
    return finish_df


#
def read_from_sheet(acc, sheet_url):
    while True:
        try:
            sheet = acc.open_by_url(sheet_url).sheet1
            data = sheet.get_all_records()
            break
        except:
            sleep(10)
    df = pd.DataFrame.from_dict(data)
    return df


#
def login_to_gmail(driver, login, password):
    driver.get("https://mail.google.com/")
    input_login = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    input_login.send_keys(login)
    _next = driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span')
    _next.click()
    sleep(15)
    input_password = driver.find_element(
        By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'
    )
    input_password.send_keys(password)
    _next = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span')
    _next.click()
    sleep(5)
    # Get the screen width and height
    screen_width, screen_height = pyautogui.size()

    # Calculate the center coordinates
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Move the mouse to the center of the screen
    pyautogui.moveTo(center_x, center_y)

    # Perform a click (you can adjust the button parameter, default is 'left')
    pyautogui.click()
    print("click")
    sleep(20)

def close_tabs(driver):
    while len(driver.window_handles) > 1:
        try:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
        except Exception as e:
            print("close tabs", e)
            continue
        driver.switch_to.window(driver.window_handles[0])
#
def people_to_cheap(driver, sheet_url):
    close_tabs(driver)
    driver.get(sheet_url)
    sleep(5)
    for i in range(2):
        pyautogui.hotkey("ctrl", "left")
        sleep(randint(1, 2))
    pyautogui.hotkey("ctrl", "up")
    sleep(randint(1, 2))
    pyautogui.hotkey("ctrl", "space")
    sleep(randint(1, 2))
    pyautogui.hotkey("alt", "i")
    sleep(randint(1, 2))
    pyautogui.press("a")
    sleep(randint(1, 2))
    pyautogui.press("e")
    # WAIT FOR CHECKING
    sleep(10)
    pyautogui.press("right")
    sleep(randint(1, 2))
    pyautogui.press("right")
    sleep(randint(1, 2))
    pyautogui.press("right")
    sleep(randint(1, 2))
    pyautogui.write("result", interval=0.25)
    sleep(randint(1, 2))
    pyautogui.press("down")
    sleep(randint(1, 2))
    pyautogui.write("=a2=b2")
    sleep(randint(1, 2))
    pyautogui.press("enter")
    sleep(randint(1, 2))
    pyautogui.press("up")
    sleep(randint(1, 2))
    pyautogui.hotkey("ctrl", "c")
    sleep(randint(1, 2))
    pyautogui.hotkey("ctrl", "shift", "down")
    sleep(randint(1, 2))
    pyautogui.hotkey("ctrl", "v")
    sleep(randint(1, 2))
    # pyautogui.hotkey("ctrl","down")
    # sleep(randint(1,2))
    # pyautogui.press('left')
    # sleep(randint(1,2))
    # pyautogui.hotkey('ctrl', "up")
    # sleep(randint(1,2))
    # pyautogui.press("down")
    # sleep(randint(1,2))
    # pyautogui.press("right")
    # sleep(randint(1,2))
    # pyautogui.hotkey('ctrl', "shift", 'down')
    # sleep(randint(1,2))
    # pyautogui.press('backspace')
    # sleep(randint(1,2))
    # for i in range(3):
    #    pyautogui.hotkey('ctrl', "up")
    #    sleep(randint(1,2))


#
def init_selenium():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--start-fullscreen")
    driver = uc.Chrome(
        driver_executable_path="driver/chromedriver", options=chrome_options
    )
    return driver


def csv_to_dict(file):
    # Check if the file exists
    if not os.path.exists(file):
        # Create an empty DataFrame with specified columns
        empty_df = pd.DataFrame(
            columns=[
                "original domain",
                "companyUrl",
                "good",
                "fullName",
                "name",
                "surname",
                "userUrl",
                "position",
                "keyword",
                "employee count",
                "company name",
                "country",
                "email",
                "priority",
                "favorite",
                "fake",
                "domain",
                "variant 1",
                "variant 2",
                "variant 3",
                "variant 4",
                "variant 5",
                "variant 6",
                "variant 7",
                "variant 8",
                "variant 9",
            ]
        )
        # Write the empty DataFrame to the file
        empty_df.to_csv(file, index=False)

    # Read the CSV file into a DataFrame
    in_data = pd.read_csv(file)
    return in_data


#
def dict_to_list(dct):
    res = []
    for key in dct:
        res.extend(dct[key])
    return res


#
def create_posistion_csv(input_file):
    df = pd.read_csv(input_file)
    positions = df["position_1"].dropna()
    final_positions = []
    for pos in positions:
        comma_split = pos.split(",")
        for com_spl in comma_split:
            _positions = com_spl.split("=")
            for one_pos in _positions:
                if one_pos.strip() not in final_positions:
                    final_positions.append(one_pos.strip())

    pd.DataFrame(
        {
            "position": final_positions,
            "priority": [i + 1 for i in range(len(final_positions))],
        }
    ).to_csv("position_priority.csv", index=False)
    return True


# create_posistion_csv("data/input_2.csv")
