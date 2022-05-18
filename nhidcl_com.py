from pkg_resources import IMetadataProvider
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import datetime
import glob
import shutil
import sqlite3
import pyodbc
import logging
from zipfile import ZipFile

link= 'https://nhidcl.com/current-tenders/'
def folder_name():
    folder=str(link).split("//")
    folder="/".join(folder)
    folder=folder.split("/")
    folder=folder[1].replace(".",'_')
    return folder

logging.basicConfig(filename=str(folder_name())+".log",format='%(asctime)s %(message)s',filemode='a',level=logging.INFO)

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


driver=webdriver.Chrome(chrome_options=chrome_options,)
logging.info(":----------------->browser is activate")
driver.get(link)
logging.info(f":browser activate Link {link}")
time.sleep(1)
driver.implicitly_wait(10)
#driver.maximize_window()
def pdf_download(all_link,text1):
    try:
        for url in all_link:
           # driver.execute_script(f"window.open('{url}');")
            url.click()
            time.sleep(2)
    except Exception as E:
        print(E)
        logging.error(text1,"error come in pdf downloaded time ------->",E)

def data_insert_in_server(list1):
    sql = f"INSERT INTO {str(folder_name())} (Tender_Summery,Bid_deadline_2,Pur_Add,Documents_2,createdOn) VALUES(?,?,?,?,?)"
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
    
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT Tender_Summery,Pur_Add,Documents_2,Bid_deadline_2 FROM {str(folder_name())} WHERE plaging=?",(1,))
        data60=cur.fetchall()
        #data60 ==all data
    except Exception as E:
        print(E,'get data from sqlit3 error')
        logging.error(f'Error come data fetchall time {E}')
    try:
        #print(pyodbc.drivers())
        connect = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                'Server=153TESERVER;'
                                'Database=CrawlingDB;'
                                'UID=amit;'
                                'PWD=amit@123;')
        logging.info('connection main database server successfully ')
        cursor = connect.cursor()
        print(connect)
    except Exception as E:
        print(E,'server connection  in  database error')
        logging.error(f"server database connect Error {E}")
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
        print(E)
        logging.error(f" server table Create Error {E}")

    try:
        #insert data in table 
        for task2 in data60:
            print(task2)
            #tasklink=task2[3].replace('\\','\\a')
            sql2=f'''INSERT INTO {str(folder_name())} (Tender_Summery,Pur_Add,Documents_2,Bid_deadline_2) VALUES (?,?,?,?)'''
            print(sql2)
            cursor.execute(sql2,task2)
            connect.commit()
            print("data insert in main database !!!!!")
            #logging.error("data insert in server database !!!!!")
        cursor.close()
        connect.close()

    except Exception as E:
        print(E)
        logging.error(f"{task2[0]} data insert error in server {E}")
    try:
        cur.execute(f"UPDATE {str(folder_name())} SET plaging=? WHERE plaging=?",(0,1,))
        conn.commit()
        logging.info("data update successfully")
    except Exception as E:
        print(E)
        logging.error(f"sqlit3 update error {E}")




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
        logging.info(f"check current folder pdf error {E}")

def pdf_rename(pdfrname,text1):
    if len(pdfname)==1:
        try:
            for rn in pdfrname:
                path=str(file_name2())+".pdf"
                os.rename(str(rn),path)
                time.sleep(1)
                shutil.move(path, zippath)
                time.sleep(1)
            return zippath+"\\"+path

        except Exception as E:
            print(E)
            logging.error(E)
            logging.error(f"{text1} pdf rename failed ")
    else:
        zpath=zippath+"\\"+str(file_name2())+'.zip'
        with ZipFile(zpath, 'w') as zipObj2:
            for url in pdfname:
                print(url)
                path=str(file_name2())+".pdf"
                try:
                    os.rename(str(url),path)
                    time.sleep(1)
                    zipObj2.write(path)
                    os.remove(path)
                except Exception as E:
                    print(E)
                    logging.error(E)
                    logging.error(f"{text1} zip create error ")
            return zpath

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

def check_data_table(text1,Bid_deadline_2):
    cur = conn.cursor()
    try:
        logging.info("check Data is duplicate Ro Not ")
        # print(text1,Bid_deadline_2)
        #cur.execute(f'''SELECT EXISTS(SELECT * FROM tender_table WHERE Tender_Notice_No='{id}');''')
        cur.execute(f"SELECT Tender_Notice_No FROM {str(folder_name())} WHERE Tender_Summery=? and Bid_deadline_2=?",(text1,Bid_deadline_2,))
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




driver.maximize_window()
pageelelink=driver.find_element(By.XPATH,'//*[@id="current_tender"]')
src=pageelelink.get_property('src')
driver.get(src)
logging.info(f"get original link from website {src}")
c=1
while True:
    try:
        print(c)
        logging.info("start scraping ")
        tr=driver.find_element(By.XPATH, '//*[@id="dataTables-example"]/tbody').find_elements(By.TAG_NAME,'tr')
        orginal_list=[]
        for i in range(len(tr)):
            tender_summ=tr[i].find_element(By.XPATH,f'//*[@id="dataTables-example"]/tbody/tr[{i+1}]/td[2]')
            text1=tr[i].find_elements(By.TAG_NAME,'td')[1].text.split('For Details  Click Here')[0].strip()
            a=tender_summ.find_elements(By.TAG_NAME,'p a')
            tem_list=[k.text.split('-')[0] for k in a]
            logging.info('check Tender is Corrigendum or not')
            if 'Corrigendum' in tem_list:
                continue
            else:

                tem_list=[]
                tem_list.append(text1)
                Bid_deadline_2=tender_summ.find_element(By.XPATH,f'//*[@id="dataTables-example"]/tbody/tr[{i+1}]/td[4]').get_attribute('innerHTML').split("<br>")[0].strip()
                tem_list.append(Bid_deadline_2)
                create_table()
                ch=check_data_table(text1,Bid_deadline_2)
                if ch==True:
                    logging.info(f"Tender_Summery =>{text1}")
                    pur_add=tender_summ.find_element(By.XPATH,f'//*[@id="dataTables-example"]/tbody/tr[{i+1}]/td[3]').text.strip()
                    logging.info(f"pur_add=>{pur_add}")
                    tem_list.append(pur_add)
                    tem_link=tender_summ.find_elements(By.TAG_NAME,'a')
                    #all_link=[lk.get_attribute('href') for lk in tem_link]
                    pdf_download(tem_link,text1)
                    check_dir(tem_link)
                    pdfname=glob.glob("*.pdf")
                    path2=pdf_rename(pdfname,text1)
                    logging.info(f"pdf download this path {path2}")
                    tem_list.append(str(path2).replace('\\','/'))
                    createdOn=str(file_name())
                    logging.info(f'createdOn=>{createdOn}')
                    tem_list.append(createdOn)
                    print(tem_list,'++++++++++++')
                    logging.info(f'scraping one row {tem_list}')
                    orginal_list.append(tuple(tem_list))
                else:
                    print("data is available in database")
                    logging.info("data is available in database")

        if ch==True:

            data_insert_in_server(orginal_list)
        nextpage=driver.find_element(By.XPATH,'//*[@id="dataTables-example_next"]').get_attribute("class")
        if 'paginate_button next disabled'==nextpage:
            logging.info("quit driver")
            conn.close()
            driver.quit()
            break
        else:
            driver.find_element(By.XPATH,'//*[@id="dataTables-example_next"]/a').click()
            logging.info("GOTO Next Page ->")
            c+=1
    except Exception as E:
        print(E)
        logging.error(E)
