import email
from locale import currency
from venv import create
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import wget
import os
import logging
import datetime
from zipfile import ZipFile
import csv
import time
import sqlite3
import unicodedata 

def folder_name():
    folder=str(link).split("//")
    folder="/".join(folder)
    folder=folder.split("/")
    folder=folder[1].replace(".",'_')
    return folder


# def csv_file_create(rows):
#     if os.path.exists(str(folder_name())+".csv"):
#         if os.stat(str(folder_name())+".csv").st_size==0:
#             try:
#                 test2=['']
#                 with open(str(folder_name())+".csv",'a', newline="") as csvfile:
#                     csvw=csv.writer(csvfile)
#                     csvw.writerow(test2)
#                     csvw.writerow(rows)
#                     logger.info(":Data Insert successfully in CSV File")
#             except Exception as E:
#                 logger.error(E)
#                 logger.error(f"{rows[0]}Data does not insert in CSV File ")
#                 print(E)
#         else:
#             try:
#                 with open(str(folder_name())+".csv",'a', newline="") as csvfile:
#                     csvw=csv.writer(csvfile)
#                     csvw.writerow(rows)
#                     logger.info(":Data Insert successfully in CSV File")
#             except Exception as E:
#                 logger.error(E)
#                 logger.error(f"{rows[0]}Data does not insert in CSV File ")
#                 print(E)
#     else:
#         try:
#             with open(str(folder_name())+".csv",'a', newline="") as csvfile:
#                 csvw=csv.writer(csvfile)
#                 csvw.writerow(test2)
#                 csvw.writerow(rows)
#                 logger.info(":Data Insert successfully in CSV File")
#                 # for i in rows: 
#                 #     csvw.writerow(i)
#         except Exception as E:
#             logger.error(E)
#             logger.error(f"{rows[0]}Data does not insert in CSV File ")
#             print(E)  

def file_name():
    date_time=str(datetime.datetime.now())
    return datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y")

def create_table():
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS 
                        tender_table (Purchaser_Name VARCHAR(200) NOT NULL,
                                    Pur_Email VARCHAR(200) NOT NULL,
                                    offfice_Address VARCHAR(200)  NOT NULL,
                                    Tender_Notice_No VARCHAR(200) NOT NULL,
                                    tender_type  VARCHER(200) NOT NULL,
                                    actualvlue  VARCHER(200) NOT NULL,
                                    Bid_Deadline VARCHER(200) NOT NULL,
                                    OpeningDate VARCHER(200) NOT NULL,
                                    bidtitle VARCHER(200) NOT NULL,
                                    created_no VARCHER(200) NOT NULL,
                                    currency VARCHER(200) NOT NULL,
                                    plaging INTEGER DEFAULT 1
                                    );''')
        #print('table')
    except Exception as E:
        print(E)
def insert_data_table(database_rows):
    task=tuple(database_rows)
    sql = f''' INSERT INTO tender_table (Purchaser_Name,Pur_Email,offfice_Address,Tender_Notice_No,tender_type,actualvlue,Bid_Deadline,OpeningDate,bidtitle,created_no,currency) VALUES{task}'''
    #d=check_data_table(task)
    d=True
    if d==True:
        try:
            cur = conn.cursor()
            cur.execute(sql)
           # logger.info("Data insert in database")
            conn.commit()
            print("insert data")
            #csv_file_create(database_rows)
            #data_insert_server()
        except Exception as E:
           # logger.error(E)
           # logger.info(f"{database_rows}Data does not insert in database")
           print(E)
    else:
        print("data is available in database")

def check_data_table(li):
    cur = conn.cursor()
    try:
        #logger.info("check Data is duplicate Ro Not ")
        open_date=li[0]
        des=li[1]
        id1=li[2]
        #print(type(id1))
        print(open_date,des,id1)
        #cur.execute(f'''SELECT EXISTS(SELECT * FROM tender_table WHERE Tender_Notice_No='{id}');''')
        cur.execute("SELECT Tender_Notice_No FROM tender_table WHERE Tender_Notice_No = ? and OpeningDate=? and bidtitle=?",(id1,open_date,des))
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
        #logger.error(E)
        #logger.info('Check data dublication error')
        print(E)






chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach',True)
chrome_options.add_argument("user-data-dir=C:\\Path")
driver=webdriver.Chrome(chrome_options=chrome_options)
link= 'https://sppp.rajasthan.gov.in/sppp/index.php'
driver.get(link)
conn = sqlite3.connect('test.db')
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="latest_active_bid"]/a')))
element.click()
#print(driver.current_url)
#driver.get(driver.current_url) //*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]
while True:
    time.sleep(1)
    row=driver.find_elements(By.XPATH,value='//*[@id="examplesearch"]/tbody/tr')
    for i in row:
        tem_list_CHECK=[]
        open_date=i.find_element(By.CSS_SELECTOR,value='#examplesearch > tbody > tr > td:nth-child(4)')
        #print(open_date.text)
        open_date=open_date.text
        #print(open_date,'++++++++++++++++++++++++++++++++++++')
        tem_list_CHECK.append(open_date)
        des=i.find_element(By.CSS_SELECTOR,value='#examplesearch > tbody > tr > td:nth-child(5)')
        des=des.get_attribute("innerHTML").split('<a')
        des=des[0].replace(',','')
        print(des,'++++++++++++++++++++++++++++++++++++++++++')
        tem_list_CHECK.append(des)
        id1=i.find_element(By.CSS_SELECTOR,value='#examplesearch > tbody > tr> td:nth-child(5) > a')
        #print(id.text)
        id1=id1.text
        print(type(id1))
        tem_list_CHECK.append(id1)
        link=i.find_element(By.TAG_NAME,value='td a')
        link.click()
        window=driver.window_handles[1]
        driver.switch_to.window(window_name=window)
        #print(tem_list_CHECK)
        create_table()
        ch=check_data_table(tem_list_CHECK)
        if ch==True:
            li=[]
            Purchaser_Name=driver.find_element(By.XPATH,value='//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]')
            #print(Purchaser_Name.text,"--------------------------Purchaser_Name---------------------------")
            li.append(Purchaser_Name.text)
            email_id=driver.find_element(By.XPATH,value='//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[5]/td[2]').text.split(' ')
            email_id=(email_id[1].replace('[at]','@')).replace('[dot]','.')
            #print(email_id,'-----------------------------------------email----------------------------')
            li.append(email_id)
            address=driver.find_element(By.XPATH,value='//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[6]/td[2]').text
            address=address.replace(',','')
            #print(address,'---------------------------------------------address-----------------------------------')
            li.append(address)
            Tender_Notice_No =driver.find_element(By.XPATH,value='//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr[2]/td[2]').text
            #print(Tender_Notice_No,'-----------------------------------------------------tender_no')
            li.append(Tender_Notice_No.strip())
            tender_type=driver.find_element(By.XPATH,value='//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr[4]/td[2]')
            #print(tender_type.text,'-------------------------------------------tender_type----------------------------')
            li.append(tender_type.text)
            actualvalue=driver.find_element(By.XPATH,value='//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr[7]/td[2]')
            #print(actualvalue.text,'---------------------------------------actualvlue----------------------------------')
            li.append(actualvalue.text)
            Bid_Deadline=driver.find_element(By.XPATH,value='//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr[17]/td[2]')
            #print(Bid_Deadline.text,'--------------------------------------Bid_Deadline----------------------------')
            li.append(Bid_Deadline.text)
            tr=driver.find_elements(By.XPATH,value='//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr')
            tr=len(tr)-3
            print(tr)
            OpeningDate=driver.find_element(By.XPATH,value='//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr['+str(tr)+']/td[2]')
            print(OpeningDate.text,'--------------------------------opening data')
            pi=OpeningDate.text.split('  ')
            #print(pi[0],'+++++++++++++++++++++++++++++++++++')
            li.append(pi[0])
            title=driver.find_element(By.XPATH,value='//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr[3]/td[2]')
            title=title.text.replace(',','')
            pititle=title.split(' ')
            pititle.remove('')
            pititle=' '.join(pititle)
            print(pititle,'=++++++++++++++++++++++++++')
            # title=(pititle)
            print(title,'-----------------------------------------------title-----------------------------')
            li.append(pititle.strip())
            created_on=file_name()
            li.append(created_on)
            #print(created_on,'------------------------------------------------------created_no-------------------------------')
            currencys='currency = INR'
            #print(currencys,'--------------------------------------------currencys-----------------------------------------------')
            li.append(currencys)
            #print(li)
         
            insert_data_table(li)
            driver.close()#//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr[3]/td[2]
            window=driver.window_handles[0]
            driver.switch_to.window(window_name=window)
        else:
            print('data is available')
            driver.close()
            window=driver.window_handles[0]
            driver.switch_to.window(window_name=window)
      
    print('nextpage',driver.current_url)
    nextpage=driver.find_element(By.XPATH,value='//*[@id="examplesearch_next"]').click()


