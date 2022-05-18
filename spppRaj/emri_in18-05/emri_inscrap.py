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

link= 'http://www.emri.in/tender-details-2/'
def folder_name():
    folder=str(link).split("//")
    folder="/".join(folder)
    folder=folder.split("/")
    folder=folder[1].replace(".",'_')
    return folder

logging.basicConfig(filename=str(folder_name())+".log",format='%(asctime)s %(message)s',filemode='a',level=logging.INFO)


def file_name2():
    date_time=str(datetime.datetime.now())
    return datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f").strftime("%d%m%Y_%H%M%S.%f")
def file_name():
    date_time=str(datetime.datetime.now())
    return datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f").strftime("%d/%m/%Y")


chrome_options = webdriver.ChromeOptions()
current_folder=os.getcwd()
zippath=os.path.expanduser('~')+"\\Documents\\pythonfile\\"+str(folder_name())+"\\files"
if os.path.isdir(zippath):
    pass
else:
    os.makedirs(zippath)
chrome_options.add_experimental_option('prefs', {
"download.default_directory": current_folder, #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})
try:
    conn = sqlite3.connect(str(folder_name())+'.db')
    logging.info('Database connection successfully ')
except Exception as E:
    logging.error(":Database connection failed")
    print(E)

ab=os.path.basename(__file__)
logging.info("File name ------->"+str(ab))
driver=webdriver.Chrome(chrome_options=chrome_options,)
path=os.getcwd()
logging.info(":----------------->browser is activate")
driver.get(link)
logging.info(f":browser activate Link {link}")
time.sleep(1)


def pdf_rename(pdfrname,text1):
    try:
        
        for rn in pdfrname:
            path=str(file_name2())+".pdf"
            os.rename(str(rn),path)
            time.sleep(0.5)
            shutil.move(path, zippath)
        return zippath+"\\"+path

    except Exception as E:
        print(E)
        logging.error(f"{text1} pdf doenload failed ")


def data_insert_in_server(text1,createdOn,path2):
    sql = f''' INSERT INTO {str(folder_name())} (Tender_Summery,createdOn,Documents_2) VALUES("{text1}", "{createdOn}", "{path2}")'''
    print(sql)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("insert data")
        logging.info("Insert data in database ")
    except Exception as E:
        print(E,'data inser in sqlite3 error ')
        logging.error(f"'{text1}:-sqlite3 data insert error-------->{E}'")
    
    # try:
    #     cur = conn.cursor()
    #     cur.execute(f"SELECT Tender_Summery,Documents_2 FROM {str(folder_name())} WHERE plaging=?",(1,))
    #     data60=cur.fetchall()
    #     #data60 ==all data
    # except Exception as E:
    #     print(E,'get data from sqlit3 error')
    #     logging.error(f'Error come data fetchall time {E} ')
    # try:
    #     #print(pyodbc.drivers())
    #     connect = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
    #                             'Server=153TESERVER;'
    #                             'Database=CrawlingDB;'
    #                             'UID=amit;'
    #                             'PWD=amit@123;')
    #     logging.info('connection main database server successfully ')
    #     cursor = connect.cursor()
    #     print(connect)
    # except Exception as E:
    #     print(E,'server connection  in  database error')
    #     logging.error(f"server database connect Error {E}")
    # try:
    #     cursor.execute(f"""IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{str(folder_name())}' AND xtype='U')
    #                                                                                                             CREATE TABLE {str(folder_name())} (
    #                                                                                                                                                 Id INTEGER IDENTITY(1,1) PRIMARY KEY ,
    #                                                                                                                                                 Tender_Notice_No TEXT,
    #                                                                                                                                                 Tender_Summery TEXT,
    #                                                                                                                                                 Tender_Details TEXT,
    #                                                                                                                                                 Bid_deadline_2 TEXT,
    #                                                                                                                                                 Documents_2 TEXT,
    #                                                                                                                                                 TenderListing_key TEXT,
    #                                                                                                                                                 Notice_Type TEXT,
    #                                                                                                                                                 Competition TEXT,
    #                                                                                                                                                 Purchaser_Name TEXT,
    #                                                                                                                                                 Pur_Add TEXT,
    #                                                                                                                                                 Pur_State TEXT,
    #                                                                                                                                                 Pur_City TEXT,
    #                                                                                                                                                 Pur_Country TEXT,
    #                                                                                                                                                 Pur_Email TEXT,
    #                                                                                                                                                 Pur_URL TEXT,
    #                                                                                                                                                 Bid_Deadline_1 TEXT,
    #                                                                                                                                                 Financier_Name TEXT,
    #                                                                                                                                                 CPV TEXT,
    #                                                                                                                                                 scannedImage TEXT,
    #                                                                                                                                                 Documents_1 TEXT,
    #                                                                                                                                                 Documents_3 TEXT,
    #                                                                                                                                                 Documents_4 TEXT,
    #                                                                                                                                                 Documents_5 TEXT,
    #                                                                                                                                                 currency TEXT,
    #                                                                                                                                                 actualvalue TEXT,
    #                                                                                                                                                 TenderFor TEXT,
    #                                                                                                                                                 TenderType TEXT,
    #                                                                                                                                                 SiteName TEXT,
    #                                                                                                                                                 createdOn TEXT,
    #                                                                                                                                                 updateOn TEXT,
    #                                                                                                                                                 Content TEXT,
    #                                                                                                                                                 Content1 TEXT,
    #                                                                                                                                                 Content2 TEXT,
    #                                                                                                                                                 Content3 TEXT,
    #                                                                                                                                                 DocFees TEXT,
    #                                                                                                                                                 EMD TEXT,
    #                                                                                                                                                 OpeningDate TEXT,
    #                                                                                                                                                 Tender_No TEXT,
    #                                                                                                                                                 )""")
    #     connect.commit()
    # except Exception as E:
    #     print(E)
    #     logging.error(f" server table Create Error {E}")

    # try:
    #     #insert data in table 
    #     for task2 in data60:
    #         print(task2)
    #         #tasklink=task2[3].replace('\\','\\a')
    #         sql2=f'''INSERT INTO {str(folder_name())} (Tender_Summery,Documents_2) VALUES ('{task2[0]}', '{task2[1]}')'''
    #         print(sql2)
    #         cursor.execute(sql2)
    #         connect.commit()
    #         print("data insert in main database !!!!!")
    #         logging.error("data insert in server database !!!!!")
    #     cursor.close()
    #     connect.close()

    # except Exception as E:
    #     print(E)
    #     logging.error(f"{i[0]} data insert error in server {E}")
    # try:
    #     cur.execute(f"UPDATE {str(folder_name())} SET plaging=? WHERE plaging=?",(0,1,))
    #     conn.commit()
    #     logging.info("data update successfully")
    # except Exception as E:
    #     print(E)
    #     logging.error(f"sqlit3 update error {E}")
    


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

def check_data_table(li):
    cur = conn.cursor()
    try:
        logging.info("check Data is duplicate Ro Not ")
        #print(type(id1))
        #cur.execute(f'''SELECT EXISTS(SELECT * FROM tender_table WHERE Tender_Notice_No='{id}');''')
        cur.execute(f"SELECT Tender_Notice_No FROM {str(folder_name())} WHERE Tender_Summery=?",(li,))
        data60=cur.fetchone()
        # for i in data60:
        #     print(i[7]==open_date1,i[3]==id1,i[8]==des1)
        #     #print(i[3],i[7],i[8])
        #     #print(i)
        #     break
        if data60 is None:
            c=True
        else:
            c=False
        return c

    except Exception as E:
        logging.error(E)
        logging.error('Check data dublication error')
        print(E)
def check_dir(pdf1):
    try:

        print('data')
        p=glob.glob("*.pdf")
        if p==[]:
            time.sleep(1)
            check_dir(pdf1)
        else:
            print(len(pdf1),len(p))
            if len(pdf1)==len(p):
                return p
            else:
                time.sleep(1)
                check_dir(pdf1)
    except Exception as E:
        print(E)





#driver.maximize_window()
try:

    data=driver.find_element(By.XPATH,'//*[@id="content"]/article/div[2]/div')
    classname=data.find_elements(By.CLASS_NAME,'sc_accordion_content')
    create_table()
    tem_list=[]
    for i in classname:
        li=i.find_elements(By.TAG_NAME,'li')
        if li==[]:
            pass
        else:
            for i in li:
                tem_list2=[]
                #print(i.get_attribute('innerHTML'))
                a=i.find_element(By.TAG_NAME,'a')
                text1=a.get_attribute('innerHTML')
                text1=text1.replace(',',' ').strip()
                ch=check_data_table(text1)
                if ch==True:
                    logging.info(f"Scraping data from website :-{text1}")
                    tem_list2.append(text1)
                    print(type(text1))
                    url=a.get_attribute('href')
                    response = requests.get(url)
                    print(response.status_code)
                    logging.info(f"PDF url {url}")
                    driver.execute_script(f"window.open('{url}');")
                    check_dir('1')
                    pdfname=glob.glob("*.pdf")
                    #print(pdfname)
                    path2=pdf_rename(pdfname,text1)
                    print(path2)
                    logging.info(f"pdf download path {path2} ")
                    createdOn =str(file_name())
                    print(createdOn)

                    # tem_list2.append(str(file_name()))
                    # tem_list2.append(path2)
                    # tem_list.append(tem_list2)
                    data_insert_in_server(text1,createdOn,path2)
                else:
                    print('data is available in database')
                    logging.info(f'{text1} :data is available in database')
    conn.close()
    driver.quit()
except Exception as E:
    print(E)
    logging.error(E)
    



            

            

