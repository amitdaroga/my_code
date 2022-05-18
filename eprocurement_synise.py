from selenium import webdriver
from selenium.webdriver.common.by import By
import wget
import time
import os
import requests
import datetime
import glob
import shutil
import sqlite3
import pyodbc
import logging


link= 'https://eprocurement.synise.com/indexx.asp'
chrome_options = webdriver.ChromeOptions()
def folder_name():
    folder=str(link).split("//")
    folder="/".join(folder)
    folder=folder.split("/")
    folder=folder[1].replace(".",'_')
    return folder

logging.basicConfig(filename=str(folder_name())+".log",format='%(asctime)s %(message)s',filemode='a',level=logging.INFO)
driver=webdriver.Chrome(chrome_options=chrome_options,)
logging.info(":----------------->browser is activate")
driver.get(link)
logging.info(f":browser activate Link {link}")
time.sleep(1)


try:
    conn = sqlite3.connect(str(folder_name())+'.db')
    logging.info('Database connection successfully ')
except Exception as E:
    logging.error(":Database connection failed")
    print(E)
ab=os.path.basename(__file__)
logging.info("File name ------->"+str(ab))
def file_name():
    date_time=str(datetime.datetime.now())
    return datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f").strftime("%d/%m/%Y")

def create_table():
    try:
        conn.execute(f'''CREATE TABLE IF NOT EXISTS 
                        {str(folder_name())} (
                                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    Tender_Notice_No TEXT,
                                    Tender_Summery TEXT,
                                    Tender_Details TEXT,
                                    Bid_deadline_2 TEXT,
                                    Documents_2 TEXT,
                                    TenderListing_key TEXT,
                                    Notice_Type TEXT,
                                    Competition TEXT,
                                    Purchaser_Name TEXT,
                                    Pur_Add TEXT,
                                    Pur_State TEXT,
                                    Pur_City TEXT,
                                    Pur_Country TEXT,
                                    Pur_Email TEXT,
                                    Pur_URL TEXT,
                                    Bid_Deadline_1 TEXT,
                                    Financier_Name TEXT,
                                    CPV TEXT,
                                    scannedImage TEXT,
                                    Documents_1 TEXT,
                                    Documents_3 TEXT,
                                    Documents_4 TEXT,
                                    Documents_5 TEXT,
                                    currency TEXT,
                                    actualvalue TEXT,
                                    TenderFor TEXT,
                                    TenderType TEXT,
                                    SiteName TEXT,
                                    createdOn TEXT,
                                    updateOn TEXT,
                                    Content TEXT,
                                    Content1 TEXT,
                                    Content2 TEXT,
                                    Content3 TEXT,
                                    DocFees TEXT,
                                    EMD TEXT,
                                    OpeningDate TEXT,
                                    Tender_No TEXT,
                                    plaging INTEGER DEFAULT 1
                                    );''')
    except Exception as E:
        print(E,'table')
        logging.error(F"Error come in table create in sqlit3 time !! {E}")


def check_data_table(TenderNoticeNo,Text1,Biddeadline2):
    cur = conn.cursor()
    try:
        #cur.execute(f'''SELECT EXISTS(SELECT * FROM tender_table WHERE Tender_Notice_No='{id}');''')
        cur.execute(f"SELECT Tender_Notice_No FROM {str(folder_name())} WHERE Tender_Notice_No=? and Tender_Summery=? and Bid_deadline_2=?",(TenderNoticeNo,Text1,Biddeadline2,))
        data60=cur.fetchone()
        if data60 is None:
            c=True
        else:
            c=False
        return c

    except Exception as E:
        print(E)
        logging.error(f"duplication of data is checking {E}")

def data_insert_in_database(database_rows):
    task=tuple(database_rows)
    sql = f''' INSERT INTO {str(folder_name())} (Tender_Notice_No,Tender_Summery,TenderType,OpeningDate,EMD,Bid_deadline_2,DocFees,createdOn) VALUES{task}'''
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        logging.info("Insert data in database ")
        print("insert data")
    except Exception as E:
        print(E,'sqlite3 data inser error-------->')
        logging.error(f"'{database_rows[0]}sqlite3 data insert error-------->{E}'")
    
    try:
        cur.execute(f"SELECT Tender_Notice_No,Tender_Summery,TenderType,OpeningDate,EMD,Bid_deadline_2,DocFees,createdOn FROM {str(folder_name())} WHERE plaging=?",(1,))
        data60=cur.fetchall()
    except Exception as E:
        print(E)
        logging.error(f'Error come data fetchall time {E} ')
    #server connection 
    try:
        connect = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                'Server=153TESERVER;'
                                'Database=CrawlingDB;'
                                'UID=amit;'
                                'PWD=amit@123;')
        # logger.info('connection main database server successfully ')
        cursor = connect.cursor()
        logging.info("server connect successfully !")
        print(connect)
    except Exception as E:
        print(E,'database connect Error')
        logging.error(f"server database connect Error {E}")
    #create table in server 
    try:
        cursor.execute(f"""IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{str(folder_name())}' AND xtype='U')
                                                                                                        CREATE TABLE {str(folder_name())} (
                                                                                                                                            Id INTEGER IDENTITY(1,1) PRIMARY KEY ,
                                                                                                                                            Tender_Notice_No TEXT,
                                                                                                                                            Tender_Summery TEXT,
                                                                                                                                            Tender_Details TEXT,
                                                                                                                                            Bid_deadline_2 TEXT,
                                                                                                                                            Documents_2 TEXT,
                                                                                                                                            TenderListing_key TEXT,
                                                                                                                                            Notice_Type TEXT,
                                                                                                                                            Competition TEXT,
                                                                                                                                            Purchaser_Name TEXT,
                                                                                                                                            Pur_Add TEXT,
                                                                                                                                            Pur_State TEXT,
                                                                                                                                            Pur_City TEXT,
                                                                                                                                            Pur_Country TEXT,
                                                                                                                                            Pur_Email TEXT,
                                                                                                                                            Pur_URL TEXT,
                                                                                                                                            Bid_Deadline_1 TEXT,
                                                                                                                                            Financier_Name TEXT,
                                                                                                                                            CPV TEXT,
                                                                                                                                            scannedImage TEXT,
                                                                                                                                            Documents_1 TEXT,
                                                                                                                                            Documents_3 TEXT,
                                                                                                                                            Documents_4 TEXT,
                                                                                                                                            Documents_5 TEXT,
                                                                                                                                            currency TEXT,
                                                                                                                                            actualvalue TEXT,
                                                                                                                                            TenderFor TEXT,
                                                                                                                                            TenderType TEXT,
                                                                                                                                            SiteName TEXT,
                                                                                                                                            createdOn TEXT,
                                                                                                                                            updateOn TEXT,
                                                                                                                                            Content TEXT,
                                                                                                                                            Content1 TEXT,
                                                                                                                                            Content2 TEXT,
                                                                                                                                            Content3 TEXT,
                                                                                                                                            DocFees TEXT,
                                                                                                                                            EMD TEXT,
                                                                                                                                            OpeningDate TEXT,
                                                                                                                                            Tender_No TEXT,
                                                                                                                                            )""")
        connect.commit()
    except Exception as E:
        print(E,'table Error ')
        logging.error(f" server table Create Error {E}")
    try:
        for i in data60:
        #insert data in server 
            sql=f"INSERT INTO {str(folder_name())} (Tender_Notice_No,Tender_Summery,TenderType,OpeningDate,EMD,Bid_deadline_2,DocFees,createdOn) VALUES {i}"
            cursor.execute(sql)
            connect.commit()
            print("data insert in main database !!!!!")
        logging.error("data insert in server database !!!!!")
        cursor.close()
        connect.close()
    except Exception as E:
        print(E,'datainsert error ')
        logging.error(f"{i[0]} data insert error in server {E}")
    
    try:
        #sqlite3 update 1 to 0
        cur.execute(f"UPDATE {str(folder_name())} SET plaging=? WHERE plaging=?",(0,1,))
        conn.commit()
        logging.info("data update successfully")
    except Exception as E:
        print(E,'sqlit3 update error ')
        logging.error(f"sqlit3 update error {E}")
    


def scraping_function():
    tem_list=[]
    try:
        logging.info("scrapimg data from tender details page ")
        Tender_Notice_No=driver.find_element(By.XPATH,'/html/body/table/tbody/tr[1]/td/form/font/table[1]/tbody/tr[1]/td[3]/font').text
        #print(Tender_Notice_No)
        tem_list.append(Tender_Notice_No)
        Tender_Summery=driver.find_element(By.XPATH,'/html/body/table/tbody/tr[1]/td/form/font/table[1]/tbody/tr[3]/td[3]/font').text
        tem_list.append(Tender_Summery)
        TenderType=driver.find_element(By.XPATH,'/html/body/table/tbody/tr[1]/td/form/font/table[1]/tbody/tr[4]/td[3]/font').text
        tem_list.append(TenderType)
        OpeningDate=driver.find_element(By.XPATH,'/html/body/table/tbody/tr[1]/td/form/font/table[1]/tbody/tr[1]/td[6]/font').text
        tem_list.append(OpeningDate)
        EMD=driver.find_element(By.XPATH,'/html/body/table/tbody/tr[1]/td/form/font/table[2]/tbody/tr[5]/td[2]/font').text.split('R')[0]
        tem_list.append(EMD)
        Bid_deadline_2=driver.find_element(By.XPATH, '/html/body/table/tbody/tr[1]/td/form/font/table[3]/tbody/tr[6]/td[3]/font/b').text
        tem_list.append(Bid_deadline_2)
        DocFees=driver.find_element(By.XPATH,'/html/body/table/tbody/tr[1]/td/form/font/table[2]/tbody/tr[7]/td[2]/font').text.split('R')[0]
        tem_list.append(DocFees)
        createdOn=str(file_name())
        tem_list.append(createdOn)
        print(tem_list)
        data_insert_in_database(tem_list)
        driver.close()
        window=driver.window_handles[0]
        driver.switch_to.window(window_name=window)
    except Exception as E:
        print(E)
        logging.error(E) 
    
try:
    logging.info(f":Scraping Table  Data")
    tbody=driver.find_element(By.XPATH,'//*[@id="tenderlink"]/div/table/tbody')
    tr=tbody.find_elements(By.TAG_NAME,'tr')
    driver.maximize_window()
except Exception as E:
    print(E)
    logging.error(f"Error come in Table body side {E}")
try:
    for i in range(1,len(tr)):
        TenderNoticeNo=tr[i].find_element(By.XPATH,f'//*[@id="tenderlink"]/div/table/tbody/tr[{str(i+1)}]/td[2]').get_attribute('innerHTML')
        print(TenderNoticeNo)
        logging.info(f":Scraping Tender_notice_no")
        TenderSummery=tr[i].find_element(By.XPATH,f'//*[@id="tenderlink"]/div/table/tbody/tr[{str(i+1)}]/td[3]/b/a')
        logging.info(f":Scraping TenderSummery ")
        Biddeadline2=tr[i].find_element(By.XPATH,f'//*[@id="tenderlink"]/div/table/tbody/tr[{str(i+1)}]/td[5]')
        logging.info("scrapimg Biddeadline2 ")
        Text1=TenderSummery.get_attribute('innerHTML')
        print(Text1.strip())
        print(Biddeadline2.text)
        logging.info(f":Scraping one cloumns data for table outpage ")
        create_table()
        kw=check_data_table(TenderNoticeNo,Text1.strip(),Biddeadline2.text)
        print(kw)
        if kw==True:
            url=TenderSummery.get_attribute('href')
            driver.execute_script(f"window.open('{url}');")
            window=driver.window_handles[1]
            driver.switch_to.window(window_name=window)
            time.sleep(1)
            logging.info("Open new Window Scraping data ")
            scraping_function()
        else:
           # sqlit_to_server()
           logging.error("data is available in database")
           print('data is available in database')
    time.sleep(1)
    page=driver.find_element(By.XPATH,'/html/body/form/table[7]/tbody/tr/td[2]/div[1]/select').find_elements(By.TAG_NAME,'option')[1].click()
except Exception as E:
    print(E)



   

