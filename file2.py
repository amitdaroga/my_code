from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions
import wget
import os
import logging
import datetime
from zipfile import ZipFile
import csv
import time
import sqlite3
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach',True)
driver=webdriver.Chrome(chrome_options=chrome_options)
link= 'https://sppp.rajasthan.gov.in/sppp/index.php'
driver.get(link)

conn = sqlite3.connect('test.db')



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
    except Exception as E:
        print(E,'table')

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
        print(li)
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





#driver.implicitly_wait(10)
# element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="latest_active_bid"]/a')))
# element.click()
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="latest_active_bid"]/a')))
element.click()
#driver.get(url)

#driver.maximize_window()
# #driver.set_page_load_timeout(10)
driver.implicitly_wait(10)
# row=driver.find_element(By.XPATH,value='//*[@id="examplesearch"]/tbody/tr')
# print(row.get_attribute("innerHTML"))
def file_name():
    date_time=str(datetime.datetime.now())
    return datetime.datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y")

#row=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/form/table/tbody/tr[5]/td/div/div[2]')))
c=2
while True:
    time.sleep(1)
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
         #driver.implicitly_wait(10)
       
            #main=driver.find_elements(By.XPATH,value="//*[text()='Department Details:']")
        if vali==True:
            link2=i.find_element(By.XPATH,f'//*[@id="examplesearch"]/tbody/tr[{po+1}]/td[8]/a').click()
            #link2.click()     
            window=driver.window_handles[1]
            driver.switch_to.window(window_name=window)
            li=[]
            Purchaser_Name=((driver.find_element(By.XPATH,value="//*[text()='Department Type']")).find_element(By.XPATH,value='..').text).replace('Department Type','').split(' ')
            Purchaser_Name.remove('')
            Purchaser_Name=' '.join(Purchaser_Name)
            li.append(Purchaser_Name)
            #________________________________________________________
            email_id=((driver.find_element(By.XPATH,value="//*[text()='Procuring Entity Contact:']")).find_element(By.XPATH,value='..').text).replace('Procuring Entity Contact:','').split(' ')
            email_id.remove('')
            email_id=(((' '.join(email_id)).replace('[at]','@')).replace('[dot]','.')).split(' ')
            li.append(email_id[1])
            #-----------------------------------------------------------
            address=((driver.find_element(By.XPATH,value="//*[text()='Office Address:']")).find_element(By.XPATH,value='..').text).replace('Office Address:','').split(' ')
            address.remove('')
            li.append((' '.join(address)).replace(',',' '))
            
            #________________________________________________________________________
            Tender_Notice_No=((driver.find_element(By.XPATH,value="//*[text()='UBN']")).find_element(By.XPATH,value='..').text).replace('UBN','').split(' ')
            Tender_Notice_No.remove('')
            li.extend((' '.join(Tender_Notice_No)).split())
            #_------------------------------------------------------------------------
            tender_type=((driver.find_element(By.XPATH,value="//*[text()='Bid Type']")).find_element(By.XPATH,value='..').text).replace('Bid Type','').split(' ')
            tender_type.remove('')
            li.extend((' '.join(tender_type)).split())
            #print(li)
            #________________________________________________________________________
            actualvalue=((driver.find_element(By.XPATH,value="//*[text()='Bid Amount']")).find_element(By.XPATH,value='..').text).replace('Bid Amount','').split(' ')
            actualvalue.remove('')
            li.extend(' '.join(actualvalue).split())
            
            #___________________________________________________________________________
            Bid_Deadline=((driver.find_element(By.XPATH,value="//*[text()='Bid Submission End Date']")).find_element(By.XPATH,value='..').text).replace('Bid Submission End Date','').split(' ')
            Bid_Deadline.remove('')
            Bid_Deadline=' '.join(Bid_Deadline)
            li.extend(Bid_Deadline.split())
    
    
            #-----------------------------------------------------------------------------
            OpeningDate=((driver.find_element(By.XPATH,value="//*[text()='Bid Open Date']")).find_element(By.XPATH,value='..').text).replace('Bid Open Date','').split(' ')
            OpeningDate.remove('')
            OpeningDate=' '.join(OpeningDate)
            li.extend(OpeningDate.split())
            
            #__________________________________________________________________________
            title=((driver.find_element(By.XPATH,value="//*[text()='Bid Title']")).find_element(By.XPATH,value='..').text).replace('Bid Title','').split(' ')
            title.remove('')
            title=(' '.join((' '.join(title)).split())).replace(',',' ')
            #li.append(OpeningDate)
            #print(li,'22222222222222222222222222222222222222222')
            title=' '.join(title.split())
            # des=' '.join(des.split())
            li.append(title)
            

            #-------------------------------------------------------------------
            created_on=file_name()
            li.append(created_on)

            #_________________________________________________
            currencys='currency = INR'
            li.append(currencys)
            print(li)
            insert_data_table(li)
            driver.close()
            window=driver.window_handles[0]
            driver.switch_to.window(window_name=window)
        else:
            print('data is available in database')
            # driver.close()
            # window=driver.window_handles[0]
            # driver.switch_to.window(window_name=window)
    print('next page')
    nextpage=driver.find_element(By.XPATH,f'//*[@id="examplesearch_next"]').click()
    print(c)
    c+=1



    
