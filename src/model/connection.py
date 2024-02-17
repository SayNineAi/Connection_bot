#
from pprint import pprint
from typing import Union
import pandas as pd
import datetime

#
from gspread_dataframe import set_with_dataframe, get_as_dataframe

from src.tools.utils.helper_functions import *
from src.tools.sheet.data_exporter import connect_to_sheet

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time


#
class ConnectLinkedin:

    #
    def __init__(self, serp_api: str, input_json, input_sheet, login, password, driver, profile, user_data_dir):
        self.user_data_dir = user_data_dir
        self.profile = profile
        self.login = login
        self.password = password
        self.driver = driver
        self.serp_api = serp_api
        self.acc = connect_to_sheet(input_json)
        self.input_sheet_url = input_sheet
        self.__init_sheets()

    def __init_sheets(self):
        self.input_sheet = self.acc.open_by_url(self.input_sheet_url)
        self.input_worksheet = self.input_sheet.worksheet("input")
        self.connection_worksheet = self.input_sheet.worksheet("connections")
        # Load the dataframes (if needed)
        self.input_df = get_as_dataframe(self.input_worksheet)
        self.connection_df = get_as_dataframe(self.connection_worksheet)

    def __init_driver(self):
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument(
            r"--user-data-dir="+self.user_data_dir)  # Update path if necessary
        options.add_argument(r'--profile-directory='+self.profile)
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable logging"])
        options.add_experimental_option("excludeSwitches", ["enable automation"])
        options.add_argument("start-maximized")

        service = Service(executable_path=self.driver)
        self.driver = webdriver.Chrome(service=service, options=options)