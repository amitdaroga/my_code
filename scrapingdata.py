# first import the all module
import requests
from bs4 import BeautifulSoup
import csv  
import os
from selenium import webdriver
import time
driver=webdriver.Chrome()
# Making a GET request

link='link you give'
data=[]
data.append(link)
while True:
    #get the url to driver
    driver.get(link)
    driver.execute_script("")
    #driver.switch_to.window(driver.window_handles[1])
    req=requests.get(link)
    soup = BeautifulSoup(req.content, 'html.parser')
    col=[i.text for i in soup.select("table thead tr th")]
    col.pop()
    r3=soup.select("table tbody tr")
    rows=[]
    #clear the data
    for i in r3:
        tem_list=[]
        for j in i:
            if j=='\n':
                pass
            else:
                j=j.text
                j=j.replace("\n"," ")
                tem_list.append(j)
        tem_list.pop()
        rows.append(tem_list)
#insert data in file 
    if os.path.exists("tender.csv"):
        if os.stat('tender.csv').st_size==0:
            with open("tender.csv",'a', newline="") as csvfile:
                csvw=csv.writer(csvfile)
                csvw.writerow(col)
                #csvw.writerows(rows)
                for i in rows:
                    csvw.writerow(i)
        else:
            with open("tender.csv",'a', newline="") as csvfile:
                csvw=csv.writer(csvfile)
                #csvw.writerows(rows)
                for i in rows:
                    csvw.writerow(i)
    else:
        with open("tender.csv",'a', newline="") as csvfile:
            csvw=csv.writer(csvfile)
            csvw.writerow(col)
            csvw.writerows(rows)
            for i in rows:
                csvw.writerow(i)
    #get the link of another page 
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    r1=[i.get("href") for i in soup.select("div ul li strong a")]
    data.extend(r1)
    if len(data)==1:
        #close the program 
        driver.close()
        break
    else:
        time.sleep(5)
        print(data[-1])
        link=data[-1]
        data=[]
# for i in data:
#     print(i.get("href"))
