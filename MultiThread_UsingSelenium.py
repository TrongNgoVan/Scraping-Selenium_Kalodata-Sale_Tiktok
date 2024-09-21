import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd
import threading
from queue import Queue

# ===============================Initial=======================================
n=6
global title_li, link_li
title_li, link_li = [], []

# ===============================Define Logic==================================

def openMultiBrowsers(n):
    drivers = []
    for i in range(n):
        driver = webdriver.Chrome("chromedriver.exe")
        drivers.append(driver)
    return drivers

def loadMultiPages(driver, n):
    # for driver in drivers:
    driver.maximize_window()
    driver.get("https://www.lazada.vn/dien-thoai-di-dong/?page={}&spm=a2o4n.home.cate_1.1.1905e182tGDwoM".format(n))
    sleep(6)

def loadMultiBrowsers(drivers_rx, n):
    for driver in drivers_rx:
        t = threading.Thread(target=loadMultiPages, args = (driver, n,))
        t.start()

def getData(driver):
    try:
        elems = driver.find_elements(By.CSS_SELECTOR , ".RfADt [href]")        
        print("Page is ready!")
    except:
        print("Please, Retry")
    for i in elems:
        title_li.append(i.text) 
        link_li.append(i.get_attribute('href'))
    sleep(3)
    driver.close()
    print("Crawl Done!!! Close browers:\n ", driver)
    print("----------------")
    return title_li, link_li

def runInParallel(func, drivers_rx):
    for driver in drivers_rx:  
        que = Queue()
        print("-------Running parallel---------")
        t1 = threading.Thread(target=lambda q, arg1: q.put(func(arg1)), args=(que, driver))
        t1.start()
    try:    
        ouput = que.get()
    except:
        ouput = [] 

    return ouput

# ===========================Run/Execute=======================================

drivers_r1 = openMultiBrowsers(n)
loadMultiBrowsers(drivers_r1, n)  
sleep(10)

# ===== GET link/title

title_link2 = runInParallel(getData, drivers_r1)

#return values
titles = title_link2[0]
links = title_link2[1]

#save to...
df_final = pd.DataFrame({'title': titles, 'link': links})
df_final.to_csv('titleLinkLazada_{}Pages.csv'.format(n))


# =============================================================================
# CONNECT TO SQL SERVER BY PYTHON
# =============================================================================
    
import pandas as pd
import pyodbc 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-RFH0PE8\SQLEXPRESS;'
                      'Database=Challenge;'
                      'Trusted_Connection=yes;')

# df = pd.read_sql_query('SELECT * FROM dbo.sales', conn)

df_final.to_sql('titleLinkLazada_{}Pages'.format(n), conn, if_exists='append')