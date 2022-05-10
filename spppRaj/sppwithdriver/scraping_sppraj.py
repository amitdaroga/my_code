from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#import wget
import os
import logging
import datetime
from zipfile import ZipFile
import csv
import time
import sqlite3
from selenium.webdriver.chrome.options import Options
import glob
#op = Options()
#prefs = {"download.default_directory" : r"C:\Users\HP\Desktop\amit","directory_upgrade":True,"extensions_to_open":""}
#p = {'prefs': {'download': {'default_directory':r'C:\Users\HP\Desktop\amit\\',"directory_upgrade":True,"extensions_to_open":""}}}
link= 'https://sppp.rajasthan.gov.in/sppp/index.php'
def folder_name():
    folder=str(link).split("//")
    folder="/".join(folder)
    folder=folder.split("/")
    folder=folder[1].replace(".",'_')
    return folder
current_folder=os.getcwd()
zippath=os.path.expanduser('~')+"\\Documents\\pythonfile\\"+str(folder_name())+"\\files"
if os.path.isdir(zippath):
    pass
else:
    os.makedirs(zippath)

profile = {"plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               "download.default_directory": current_folder,
               "download.extensions_to_open": "",
               "plugins.always_open_pdf_externally": True,
               "download.directory_upgrade": True
                }




chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", profile)
chrome_options.add_experimental_option('detach',True)
chrome_options.add_argument('disable-infobars')
driver=webdriver.Chrome(chrome_options=chrome_options,)
driver.maximize_window()
driver.get(link)

# def every_downloads_chrome(driver,pdf):
#         driver.get("chrome://downloads/")
#         p=driver.execute_script("""
#             return document.querySelector('downloads-manager')
#             .shadowRoot.querySelector('#downloadsList')
#             .items.filter(e => e.state === 'COMPLETE')
#             .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
#             """)
#         if p==[]:
#             every_downloads_chrome(driver,pdf)
#         else:
#             print(len(pdf),len(p))
#             if len(pdf)==len(p):
#                 clear_chrome()
#                 return p
#             else:
#                 every_downloads_chrome(driver,pdf)

                


# def clear_chrome():
#     driver.execute_script("""
#             document.querySelector('downloads-manager').shadowRoot
#             .querySelector('#toolbar').shadowRoot
#             .querySelector('#moreActionsMenu')
#             .querySelector('button.clear-all').click()
#             """)  

def refresh_error():
    textall=' '.join(driver.find_element(By.XPATH, '//*[@id="examplesearch_paginate"]/span').text.split('…')[0]).split(' ')
    print(textall)


def check_dir(pdf):
    try:

        print('data')
        p=glob.glob("*.pdf")
        if p==[]:
            time.sleep(1)
            check_dir(pdf)
        else:
            print(len(pdf),len(p))
            if len(pdf)==len(p):
                return p
            else:
                time.sleep(1)
                check_dir(pdf)
    except Exception as E:
        print(E)



conn = sqlite3.connect('test.db')

def Scraping_page():
    try:
        link2=i.find_element(By.XPATH,f'//*[@id="examplesearch"]/tbody/tr[{po+1}]/td[8]/a').click()
        #link2.click()     
        window=driver.window_handles[1]
        driver.switch_to.window(window_name=window)
        li=[]
        Purchaser_Name=((driver.find_element(By.XPATH,value="//*[text()='Department Type']")).find_element(By.XPATH,value='..'))
        #Purchaser_Name.remove('')
        #Purchaser_Name=' '.join(Purchaser_Name)
        #li.append(Purchaser_Name)
        Purchaser_Name=Purchaser_Name.find_element(By.CLASS_NAME,'data_text').text.strip()
        li.append(Purchaser_Name)
        #________________________________________________________
        Pur_Email=((driver.find_element(By.XPATH,value="//*[text()='Procuring Entity Contact:']")).find_element(By.XPATH,value='..'))#.replace('Procuring Entity Contact:','').split(' ')
        #email_id.remove('')
        Pur_Email=Pur_Email.find_element(By.CLASS_NAME,'data_text').text.replace('[at]','@').replace('[dot]','.').split(' ')
        #print(Pur_Email[1])
        #email_id=(((' '.join(email_id)).replace('[at]','@')).replace('[dot]','.')).split(' ')
        li.append(Pur_Email[1])
        #-----------------------------------------------------------
        Pur_Add=((driver.find_element(By.XPATH,value="//*[text()='Office Address:']")).find_element(By.XPATH,value='..'))#.replace('Office Address:','').split(' ')
        #address.remove('')
        Pur_Add=Pur_Add.find_element(By.CLASS_NAME,'data_text').text.replace(',',' ').strip()
        print(Pur_Add)
        li.append(Pur_Add)
        #li.append((' '.join(address)).replace(',',' '))
        
        #________________________________________________________________________
        Tender_Notice_No=((driver.find_element(By.XPATH,value="//*[text()='UBN']")).find_element(By.XPATH,value='..'))#.replace('UBN','').split(' ')
        Tender_Notice_No=Tender_Notice_No.find_element(By.CLASS_NAME, 'data_text').text.strip()
        li.append(Tender_Notice_No)
        #Tender_Notice_No.remove('')
        #li.extend((' '.join(Tender_Notice_No)).strip())
        #_------------------------------------------------------------------------
        TenderType=((driver.find_element(By.XPATH,value="//*[text()='Bid Type']")).find_element(By.XPATH,value='..'))#.replace('Bid Type','').split(' ')
        # tender_type.remove('')
        # li.extend((' '.join(tender_type)).split())
        #print(li)
        TenderType=TenderType.find_element(By.CLASS_NAME,'data_text').text.strip()
        li.append(TenderType)
        #________________________________________________________________________
        actualvalue=((driver.find_element(By.XPATH,value="//*[text()='Bid Amount']")).find_element(By.XPATH,value='..').text).replace('Bid Amount','').split(' ')
        actualvalue.remove('')
        li.extend(' '.join(actualvalue).split())
        
        #___________________________________________________________________________
        Bid_Deadline=((driver.find_element(By.XPATH,value="//*[text()='Bid Submission End Date']")).find_element(By.XPATH,value='..'))#.replace('Bid Submission End Date','').split(' ')
        #Bid_Deadline.remove('')
        #Bid_Deadline=' '.join(Bid_Deadline)
        #li.extend(Bid_Deadline.split())
        Bid_Deadline=Bid_Deadline.find_element(By.CLASS_NAME, 'data_text').text.strip()
        li.append(Bid_Deadline)


        #-----------------------------------------------------------------------------
        OpeningDate=((driver.find_element(By.XPATH,value="//*[text()='Bid Open Date']")).find_element(By.XPATH,value='..'))#.replace('Bid Open Date','').split(' ')
        #OpeningDate.remove('')
        #OpeningDate=' '.join(OpeningDate)
        #li.extend(OpeningDate.split())
        OpeningDate=OpeningDate.find_element(By.CLASS_NAME,'data_text').text.strip()
        li.append(OpeningDate)
        
        #__________________________________________________________________________
        Tender_Summery=((driver.find_element(By.XPATH,value="//*[text()='Bid Title']")).find_element(By.XPATH,value='..').text).replace('Bid Title','').split(' ')
        Tender_Summery.remove('')
        Tender_Summery=(' '.join((' '.join(Tender_Summery)).split())).replace(',',' ')
        #li.append(OpeningDate)
        #print(li,'22222222222222222222222222222222222222222')
        Tender_Summery=' '.join(Tender_Summery.split())
        # des=' '.join(des.split())
        li.append(Tender_Summery)
        

        #-------------------------------------------------------------------
        created_on=file_name()
        li.append(created_on)

        #_________________________________________________
        currencys='currency = INR'
        li.append(currencys)
        
        
        pdf=driver.find_element(By.XPATH, '//*[@id="print-this-table"]/tbody/tr[2]/td/table/tbody').find_elements(By.TAG_NAME, 'a')
        pdf_download(pdf)
        #every_downloads_chrome(driver,pdf)
        #driver.get('')
        #driver.close()
        # pdfname=glob.glob("*.pdf")
        # print(pdfname)
        # pdf_rename(pdfname)
        # create_zip()
        # pdfname1=pdfname[-1].split('\\')
        # print(pdfname1[-1])
        # os.rename(str(pdfname1[-1]),str(file_name2())+".pdf")
        #response = requests.get(pdf)
        
        #print(pdf)
        #print(li)
    except Exception as E:
        print(E)
    
    try:
        #driver.close()
        # window=driver.window_handles[2]
        # driver.switch_to.window(window_name=window)
        # driver.close()
        # window=driver.window_handles[-1]
        # driver.switch_to.window(window_name=window)
        # driver.close()
        # action = ActionChains(driver)
        # action.key_down(Keys.CONTROL).send_keys('ctrl+w').key_up(Keys.CONTROL).perform()
        driver.close()
        window=driver.window_handles[0]
        driver.switch_to.window(window_name=window)
        check_dir(pdf)
        return li
        #driver.close()
    except Exception as E:
        print(E)


def pdf_download(pdflink):
    try:
        for ik in pdflink:
            ik.click()
            time.sleep(1)
    except Exception as E:
        print(E)
def pdf_rename(pdfrname):
    try:
        for rn in pdfrname:
            os.rename(str(rn),str(file_name2())+".pdf")
            time.sleep(1)
    except Exception as E:
        print(E)
def create_zip():
    #time.sleep(3)
    try:
        pdfname_zip=glob.glob("*.pdf")
        path=str(zippath)+"\\"+str(file_name2())+".zip"
        with ZipFile(path,"w") as newzip:
            for zp in pdfname_zip: 
                newzip.write(zp)
                os.remove(zp)
            return path
    except Exception as E:
        print(E)
        #time.sleep(1)
    




def create_table():
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS 
                        tender_table (
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

def insert_data_table(database_rows):
    task=tuple(database_rows)
    sql = f''' INSERT INTO tender_table (Purchaser_Name,Pur_Email,Pur_Add,Tender_Notice_No,TenderType,actualvalue,Bid_Deadline_1,OpeningDate,Tender_Summery,createdOn,currency,Documents_2) VALUES{task}'''
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
        print(li)
        #cur.execute(f'''SELECT EXISTS(SELECT * FROM tender_table WHERE Tender_Notice_No='{id}');''')
        cur.execute("SELECT Tender_Notice_No FROM tender_table WHERE Tender_Notice_No = ? and OpeningDate=? and Tender_Summery=?",(id1,open_date,des))
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





#driver.implicitly_wait(10)
# element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="latest_active_bid"]/a')))
# element.click()
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="latest_active_bid"]/a')))
element.click()
#driver.get(url)

#driver.maximize_window()
# #
#driver.implicitly_wait(10)
# row=driver.find_element(By.XPATH,value='//*[@id="examplesearch"]/tbody/tr')
# print(row.get_attribute("innerHTML"))
def file_name():
    date_time=str(datetime.datetime.now())
    return datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y")

def file_name2():
    date_time=str(datetime.datetime.now())
    return datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f").strftime("%d%m%Y_%H%M%S.%f")

#row=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr[5]/td/div/div[2]')))
c=2
while True:
    try:
        time.sleep(1)
        #driver.set_page_load_timeout(10)
        refresh_error()
        row=driver.find_elements(By.XPATH,'//*[@id="examplesearch"]/tbody/tr')
        for po,i in enumerate(row) :
            tem_list_CHECK=[]
            open_date=i.find_element(By.XPATH,f'//*[@id="examplesearch"]/tbody/tr[{po+1}]/td[4]')
            #print(open_date.text)
            # open_date=open_date.text
            #print(open_date,'++++++++++++++++++++++++++++++++++++')
            tem_list_CHECK.append(open_date.text)
            des=' '.join(i.find_element(By.XPATH,f'//*[@id="examplesearch"]/tbody/tr[{po+1}]/td[5]').get_attribute("innerHTML").split('<a')[0].replace(',',' ').split())
            #des=des.get_attribute("innerHTML").split('<a')
            #print(des,'++++++++++++++++++++++++++++++++++++++++++')
            tem_list_CHECK.append(des)
            id1=i.find_element(By.XPATH,f'//*[@id="examplesearch"]/tbody/tr[{po+1}]/td[5]/a')
            print(id1.text)
            
            #print(type(id1))
            tem_list_CHECK.append(id1.text)
            #print(tem_list_CHECK,'1111111111111111111111111111111111111111111111111111111111111111111')
            create_table()
            vali=check_data_table(tem_list_CHECK)
            if vali==True:
                list1=Scraping_page()
                pdfname=glob.glob("*.pdf")
                print(pdfname)
                pdf_rename(pdfname)
                path2=create_zip()
                print(path2)
                list1.append(path2)
                print(list1)
                insert_data_table(list1)

            else:
                print('data is ha')
        print('next page')
        prives=driver.find_element(By.XPATH,f'//*[@id="examplesearch_next"]').get_attribute('class')
        if prives=='paginate_button next disabled':
            break
        else:
            driver.find_element(By.XPATH,f'//*[@id="examplesearch_next"]').click()
        print(c)
        c+=1
    except StaleElementReferenceException as E:
        print('error')
        driver.refresh()

    except NoSuchElementException as E:
        print('error 2')
        print(E)
        break 
    except Exception as E:
        print(E)
        break