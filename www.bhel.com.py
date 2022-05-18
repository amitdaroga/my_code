from numpy import rint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
import requests
from zipfile import ZipFile


link= 'https://www.bhel.com/tenders'
def folder_name():
    folder=str(link).split("//")
    folder="/".join(folder)
    folder=folder.split("/")
    folder=folder[1].replace(".",'_')
    return folder

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

# chrome_options.add_experimental_option('prefs', {
# "download.default_directory": current_folder, #Change default directory for downloads
# "download.prompt_for_download": False, #To auto download the file
# "download.directory_upgrade": True,
# "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
# })
#chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-gpu")

def pdf_download(pdflink,title):
    print(title)
    if len(pdflink)==1:
        for url in pdflink:
            print(url)
            ex=str(url).split('/')[-1].split('.')[-1]
            print(ex)
            path=zippath+"\\"+str(file_name2())+"."+ex
            try:
                response = requests.get(url)
                print(response.status_code)
                open(path, "wb").write(response.content)
            except Exception as E:
                print(E)
               # logger.info(f"{title} : PDF does not downloaded")
        print("--------------------------next-------------------------")
        return path
    else:
        zippath2=zippath+"\\"+str(file_name2())+'.zip'
        with ZipFile(zippath2, 'w') as zipObj2:
            for url in pdflink:
                print(url)
                ex=str(url).split('/')[-1].split('.')[-1]
                print(ex)
                path=str(file_name2())+"."+ex
                try:
                    response = requests.get(url)
                    print(response.status_code)
                    open(path, "wb").write(response.content)
                    zipObj2.write(path)
                   # logger.info(f"{title} : PDF download successfully  location :{zippath} ")
                    os.remove(path)
                except Exception as E:
                    print(E)
                   # logger.info(f"{title} : PDF does not downloaded")
                  #  logger.error(E)
            print("--------------------------next-------------------------")
            return zippath2


def data_insert_in_server(list1):
    sql = f"INSERT INTO {str(folder_name())} (Tender_Notice_No,Pur_Add,Pur_Email,TenderType,Tender_Summery,Purchaser_Name,actualvalue,EMD,DocFees,Bid_deadline_2,OpeningDate,createdOn,Documents_2) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
    print(sql)
    try:
        cur = conn.cursor()
        cur.executemany(sql,list1)
        conn.commit()
        print("insert data")
        logging.info("Insert data in database ")
    except Exception as E:
        print(E,'data inser in sqlite3 error ')
        logging.error(f"'{text1}:-sqlite3 data insert error-------->{E}'")
    
    # try:
    #     cur = conn.cursor()
    #     cur.execute(f"SELECT Tender_Notice_No,Pur_Add,Pur_Email,TenderType,Tender_Summery,Purchaser_Name,actualvalue,EMD,DocFees,Bid_deadline_2,OpeningDate,Documents_2 FROM {str(folder_name())} WHERE plaging=?",(1,))
    #     data60=cur.fetchall()
    #     #data60 ==all data
    # except Exception as E:
    #     print(E,'get data from sqlit3 error')
    #     logging.error(f'Error come data fetchall time {E}')
    # try:
    #     #print(pyodbc.drivers())
    #     connect = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
    #                             'Server=153TESERVER;'
    #                             'Database=CrawlingDB;'
    #                             'UID=amit;'
    #                             'PWD=amit@123;')
    #     logging.info('connection main database server successfully ')
    #     cursor_ser = connect.cursor()
    #     print(connect)
    # except Exception as E:
    #     print(E,'server connection  in  database error')
    #     logging.error(f"server database connect Error {E}")
    # try:
    #     cursor_ser.execute(f"""IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{str(folder_name())}' AND xtype='U')
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
    #         sql2=f'''INSERT INTO {str(folder_name())} (Tender_Notice_No,Pur_Add,Pur_Email,TenderType,Tender_Summery,Purchaser_Name,actualvalue,EMD,DocFees,Bid_deadline_2,OpeningDate,Documents_2) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''
    #         print(sql2)
    #         cursor_ser.execute(sql2,task2)
    #         connect.commit()
    #         print("data insert in main database !!!!!")
    #         #logging.error("data insert in server database !!!!!")
    #     cursor_ser.close()
    #     connect.close()

    # except Exception as E:
    #     print(E)
    #     logging.error(f"{task2[0]} data insert error in server {E}")
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

def check_data_table(ten_no,text1,OpeningDate_front_page):
    cur = conn.cursor()
    try:
        logging.info("check Data is duplicate Ro Not ")
        #print(type(id1))
        #cur.execute(f'''SELECT EXISTS(SELECT * FROM tender_table WHERE Tender_Notice_No='{id}');''')
        cur.execute(f"SELECT Tender_Notice_No FROM {str(folder_name())} WHERE Tender_Notice_No LIKE '%{ten_no}%' and Tender_Summery=? and OpeningDate=?",(text1,OpeningDate_front_page))
        data60=cur.fetchone()
        if data60 is None:
            c=True
        else:
            c=False
        return c

    except Exception as E:
        logging.error(E)
        logging.error('Check data dublication error')
        print(E)



def scraping():
    tem_list2=[]
    driver.implicitly_wait(5)
    try:
        Tender_Notice_No=driver.find_element(By.XPATH,"//*[text()='NIT NO.']").find_element(By.XPATH,'..').find_element(By.TAG_NAME,'td').text.strip()
        print(Tender_Notice_No)
        tem_list2.append(Tender_Notice_No)
    except NoSuchElementException as E:
        print("Element is not avalable Tender_Notice_No ")
        tem_list2.append('Null')
    except Exception as E:
        print(E)
    try:
        Pur_Add=driver.find_element(By.XPATH,"//*[text()='ADDRESS']").find_element(By.XPATH,'..').find_element(By.TAG_NAME,'td').text.strip()
        tem_list2.append(Pur_Add)
    except NoSuchElementException as E:
        print('Element is not avalable Pur_Add ')
        tem_list2.append('Null')
    except Exception as E:
        print(E)
    try:
        Pur_Email=driver.find_element(By.XPATH,"//*[text()='EMAIL']").find_element(By.XPATH,'..').find_element(By.TAG_NAME,'td').text.replace('[at]','@').replace('[dot]','.').strip()
        tem_list2.append(Pur_Email)
    except NoSuchElementException as E:
        print("Element is not avalable Pur_Email")
        tem_list2.append('Null')
    except Exception as E:
        print(E)
    try:
        TenderType=driver.find_element(By.XPATH,"//*[text()='TENDER TYPE']").find_element(By.XPATH,'..').find_element(By.TAG_NAME,'td').text.strip()
        tem_list2.append(TenderType)
    except NoSuchElementException as E:
        print('Element is not avalable TenderType')
        tem_list2.append('Null')
    except Exception as E:
        print(E)
    try:
        Tender_Summery=driver.find_element(By.XPATH,"//*[text()='TENDER DESCRIPTION']").find_element(By.XPATH,'..').find_element(By.TAG_NAME,'td').text.strip()
        tem_list2.append(Tender_Summery)
    except NoSuchElementException as E:
        print('Element is not avalable Tender_Summery')
        tem_list2.append('Null')
    except Exception as E:
        print(E)
    Purchaser_Name="Bharat Heavy Electricals Limited"
    tem_list2.append(Purchaser_Name)
    try:
        actualvalue=driver.find_element(By.XPATH,"//*[text()='TENDER VALUE']").find_element(By.XPATH,'..').find_element(By.TAG_NAME,'td').text.strip()
        tem_list2.append(actualvalue)
    except NoSuchElementException as E:
        print('Element is not avalable actualvalue')
        tem_list2.append('Null')
    except Exception as E:
        print(E)
    try:
        EMD=driver.find_element(By.XPATH,"//*[text()='EMD VALUE']").find_element(By.XPATH,'..').find_element(By.TAG_NAME,'td').text.strip()
        tem_list2.append(EMD)
    except NoSuchElementException as E:
        print('element is not avalable EMD')
        tem_list2.append('Null')
    except Exception as E:
        print(E)
    try:
        DocFees=driver.find_element(By.XPATH,"//*[text()='DOCUMENT VALUE']").find_element(By.XPATH,'..').find_element(By.TAG_NAME,'td').text.strip()
        tem_list2.append(DocFees)
    except NoSuchElementException as E:
        print("Element is not avalable  DocFees")
        tem_list2.append('Null')
    except Exception as E:
        print(E)
    try:
        Bid_deadline_2=driver.find_element(By.XPATH,"//*[text()='CLOSING DATE OF SUBMISSION FORM']").find_element(By.XPATH,'..').find_element(By.TAG_NAME,'td').text.split(" ")[0].strip()
        tem_list2.append(Bid_deadline_2)
    except NoSuchElementException as E:
        print("Element is not avalable Bid_deadline_2 ")
        tem_list2.append('Null')
    except Exception as E:
        print(E)
    try:
        OpeningDate =driver.find_element(By.XPATH,"//*[text()='TENDER OPENING DATE']").find_element(By.XPATH,'..').find_element(By.TAG_NAME,'td').text.split(" ")[0].strip()
        print(OpeningDate)
        tem_list2.append(OpeningDate )
    except NoSuchElementException as E:
        print("Element is not avalable OpeningDate ")
        tem_list2.append('Null')
    except Exception as E:
        print(E)
    createdOn=str(file_name())
    tem_list2.append(createdOn)
    try:
        all_link=driver.find_element(By.XPATH,"//*[text()='Download Full Details of Tender']").find_element(By.XPATH,'..').find_elements(By.TAG_NAME,'a')
        pdf_link=[i.get_attribute('href') for i in all_link]
        print(pdf_link)
        pl=pdf_download(pdf_link,ten_no)
        tem_list2.append(pl.replace('\\','/'))
    except NoSuchElementException as E:
        print("Element is not avalable pdf_link ")
        tem_list2.append('Null')
    print(tem_list2)
    print(len(tem_list2))
    orginal_list.append(tuple(tem_list2))
    driver.close()
    window=driver.window_handles[0]
    driver.switch_to.window(window_name=window)



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
current_page=1
while True:
    tr=driver.find_element(By.XPATH,'//*[@id="block-friday-content"]/div/div/div/table/tbody').find_elements(By.TAG_NAME,'tr')
    orginal_list=[]
    c=0
    for i in range(len(tr)):
        tem_list=[]
        ten_no=tr[i].find_element(By.XPATH,f'//*[@id="block-friday-content"]/div/div/div/table/tbody/tr[{i+1}]/td[2]/span[1]').text.split(':')[-1].strip()
        print(ten_no)
        tem_list.append(ten_no)
        ten_sum=tr[i].find_element(By.XPATH,f'//*[@id="block-friday-content"]/div/div/div/table/tbody/tr[{i+1}]/td[2]/span[3]/a')
        text1=ten_sum.text.strip()
        tem_list.append(text1)
        OpeningDate_front_page=tr[i].find_element(By.XPATH,f"//*[@id='block-friday-content']/div/div/div/table/tbody/tr[{i+1}]/td[4]").text.split(' ')[0].strip()
        create_table()
        ch=check_data_table(ten_no,text1,OpeningDate_front_page)
        print(ch)
        if ch==True:
            c+=1
            page_detail=ten_sum.get_attribute('href')
            driver.execute_script(f"window.open('{page_detail}');")
            window=driver.window_handles[1]
            driver.switch_to.window(window_name=window)
            scraping()
        else:
            print("data is available in database")
    if c !=0:
        data_insert_in_server(orginal_list)
    print(current_page)
    current_page +=1
    try:
        nextpage=driver.find_element(By.XPATH,"//*[text()='Next ›']").click()
    except NoSuchElementException as E:
        print(E)
        break
    except Exception as E:
        print(E)
  