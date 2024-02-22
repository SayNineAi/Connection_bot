#
from pprint import pprint
from typing import Union
import pandas as pd
import random

#
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from datetime import datetime, timedelta, date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time
from linkedin_scraper import actions
from config import CONNECT, MORE_ACTIONS, SEND_WITHOUT_NOTE, SECTION, SEND_WITHOUT_NOTE_ALL
from src.tools.utils.helper_functions import *
from src.tools.sheet.data_exporter import connect_to_sheet

import pyautogui

#
class ConnectLinkedin:

    #
    def __init__(self,
                 input_json,
                 input_sheet,
                 login,
                 password,
                 driver,
                 profile,
                 user_data_dir):
        self.user_data_dir = user_data_dir
        self.profile = profile
        self.login = login
        self.password = password
        self.driver_dir = driver
        self.acc = connect_to_sheet(input_json)
        self.input_sheet_url = input_sheet
        self.__init_sheets()
        self.__init_driver()

    def __init_sheets(self):
        self.input_sheet = self.acc.open_by_url(self.input_sheet_url)
        self.input_worksheet = self.input_sheet.worksheet("input")
        self.const_worksheet = self.input_sheet.worksheet("const")
        self.connection_worksheet = self.input_sheet.worksheet("Connections")
        # Load the dataframes (if needed)
        self.input_df = get_as_dataframe(self.input_worksheet)
        self.const_df = get_as_dataframe(self.const_worksheet)
        self.connection_df = get_as_dataframe(self.connection_worksheet)['URL']

    def __init_driver(self):
        options = Options()
        options.add_argument(
            r"--user-data-dir="+self.user_data_dir)  # Update path if necessary
        options.add_argument(r'--profile-directory='+self.profile)
        self.driver = uc.Chrome(driver_executable_path=self.driver_dir, options=options)

    def check_before_connect(self, url):
        return url in self.connection_df

    def get_from_to(self):
        # Get today's date
        today = datetime.now()
        # Calculate the start of the week (Monday)
        start_of_week = today - timedelta(days=today.weekday())
        # Format dates
        start_of_week_str = start_of_week.strftime('%Y-%m-%d')
        today_str = today.strftime('%Y-%m-%d')
        return start_of_week_str, today_str

    def connect_action(self, url) -> bool:
        try:
            print(82)
            self.driver.get(url)
            time.sleep(10)
            try:
                panding = self.driver.find_elements(By.XPATH, '//span[text()="Pending"]')
                if len(panding) > 0:
                    return "Pending"
            except:
                pass
            print(85)
            more_actions = self.driver.find_elements(By.XPATH, MORE_ACTIONS)
            if len(more_actions) != 0:
                more_actions[-1].click()
            else:
                return False
            print(92)
            time.sleep(10)
            connect = self.driver.find_elements(By.XPATH, CONNECT)
            if len(connect) != 0:
                connect[-1].click()
            else:
                section = self.driver.find_elements(By.XPATH, SECTION)[0]
                print(section.get_attribute("innerHTML"))
                connect = section.find_elements(By.XPATH, '//span[text()="Connect"]/parent::button')
                connect[1].click()
            time.sleep(10)
            time.sleep(10)
            send_without = self.driver.find_elements(By.XPATH, SEND_WITHOUT_NOTE)
            print("Send without")
            if len(send_without) == 0:
                send_without = self.driver.find_elements(By.XPATH, SEND_WITHOUT_NOTE_ALL)
            print("Send without")
            send_without[-1].click()
            time.sleep(5)
            self.update_count()
            return True

        except Exception as e:
            self.update_count()
            print(e)
            return False

    def iterate_connects(self, timeout=900):
        for index, row in self.input_df.iterrows():
            try:
                if self.check_date_count() == 200:
                    break
                pyautogui.hotkey("ctrl", "r")
                time.sleep(10)
                print(pd.isna(row['Connected']))
                if not pd.isna(row['Connected']):
                    print('connected')
                    continue
                url = row['LinkedinUrl']
                print(self.check_before_connect(url))
                if self.check_before_connect(url):
                    self.input_df.loc[index, "Comment"] = "Connected"
                    self.input_df.loc[index, "Connected"] = True
                    continue
                result = self.connect_action(url)
                self.input_df.loc[index, "Connected"] = result
                self.input_df.loc[index, "Comment"] = "Good"

                set_with_dataframe(self.input_worksheet, self.input_df)
                set_with_dataframe(self.const_worksheet, self.const_df)
                self.input_df = get_as_dataframe(self.input_worksheet)
                self.const_df = get_as_dataframe(self.const_worksheet)

                time.sleep(random.randint(600, 900))
            except Exception as e:
                print(e)
                self.input_df.loc[index, "Comment"] = "Error"
                continue

    @staticmethod
    def get_current_week_dates_str():
        """
        Returns the start and end date of the current week.
        The week starts on Monday and ends on Sunday.
        """
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_of_week_str = start_of_week.strftime('%Y-%m-%d')
        end_of_week = end_of_week.strftime('%Y-%m-%d')
        return start_of_week_str, end_of_week

    @staticmethod
    def get_current_week_dates():
        """
        Returns the start and end date of the current week.
        The week starts on Monday and ends on Sunday.
        """
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week

    def check_date_count(self):
        from_date, to_date = self.get_current_week_dates_str()
        # Check if the current week's dates exist in the dataframe
        date_exists = ((self.const_df['from'] == from_date) & (self.const_df['to'] == to_date)).any()
        print(date_exists)
        print(self.const_df)
        if date_exists:
            # Get the count for the current week
            count = self.const_df.loc[(self.const_df['from'] == from_date) & (self.const_df['to'] == to_date), 'count'].iloc[0]
            print(count)
            return count
        else:
            # Add a new row with current week's dates and count = 0
            new_row = {'from': from_date, 'to': to_date, 'count': 0}
            self.const_df.loc[len(self.const_df)] = new_row
            print(self.const_df)
            return 0

    def update_count(self):
        from_date, to_date = self.get_current_week_dates_str()
        # Update the count for the current week
        self.const_df.loc[(self.const_df['from'] == from_date) & (self.const_df['to'] == to_date), 'count'] += 1

    def start(self):
        try:
            # actions.login(self.driver, self.login, self.password)
            count = self.check_date_count()
            if count < 200:
                self.iterate_connects()
        except Exception as e:
            print(e)
        finally:
            set_with_dataframe(self.input_worksheet, self.input_df)
            set_with_dataframe(self.const_worksheet, self.const_df)
            self.driver.quit()
