from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_driver_path = "driver/chromedriver.exe"  # Update this with the actual path to your ChromeDriver

options = Options()
options.add_experimental_option("detach", True)
options.add_argument(r"--user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data")  # Update path if necessary
options.add_argument(r'--profile-directory=Profile 2')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable logging"])
options.add_experimental_option("excludeSwitches", ["enable automation"])
options.add_argument("start-maximized")


service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)


driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
time.sleep(60)  # Consider using WebDriverWait here
driver.quit()
