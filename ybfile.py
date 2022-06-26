from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import datetime
import glob
import shutil
import sqlite3
#import pyodbc
import logging
from zipfile import ZipFile


link= 'https://www.yesbank.in/about-us/media/auction-property'
def folder_name():
    folder=str(link).split("//")
    folder="/".join(folder)
    folder=folder.split("/")
    folder=folder[1].replace(".",'_')
    return folder

logging.basicConfig(filename=str(folder_name())+".log",format='%(asctime)s %(message)s',filemode='a',level=logging.INFO)

chrome_options = webdriver.ChromeOptions()
current_folder=os.getcwd()
zippath=current_folder+"\\Doc"
if os.path.isdir(zippath):
    pass
else:
    os.makedirs(zippath)
# chrome_options.add_argument('--incognito')
# chrome_options.add_argument('log-level=3')
# chrome_options.add_argument("no-first-run")
chrome_options.add_argument("--enable-javascript")
# chrome_options.add_argument("no-sandbox")
# chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("enable-automation")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(f"user-data-dir={zippath}")

# chrome_options.add_experimental_option('prefs', {
# "download.default_directory": current_folder, #Change default directory for downloads
# "download.prompt_for_download": False, #To auto download the file
# "download.directory_upgrade": True,
# "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
# })


#chrome_options.add_argument("--host-resolver-rules=MAP www.google-analytics.com 127.0.0.1")

#chrome_options.add_argument("enable-experimental-web-platform-features")


ab=os.path.basename(__file__)
logging.info("File name ------->"+str(ab))
try:
    conn = sqlite3.connect(str(folder_name())+'.db')
    logging.info('Database connection successfully ')
except Exception as E:
    logging.error(":Database connection failed")
    print(E)

def file_name2():
    date_time=str(datetime.datetime.now())
    return datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f").strftime("%d%m%Y_%H%M%S.%f")
def file_name():
    date_time=str(datetime.datetime.now())
    return datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f").strftime("%d/%m/%Y")


driver=webdriver.Chrome(r"C:\Users\HP\Downloads\Achromedriver_win32\chromedriver.exe",chrome_options=chrome_options,)
logging.info(":----------------->browser is activate")
#driver.set_page_load_timeout(30)
driver.maximize_window()
driver.get(link)
driver.implicitly_wait(10)
logging.info(f":browser activate Link {link}")
time.sleep(5)
driver.implicitly_wait(10)

time.sleep(20)



