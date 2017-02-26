

from bs4 import BeautifulSoup
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 
from selenium import webdriver
import random
import time

driver = webdriver.PhantomJS()

url="https://statesummaries.ncics.org/co"
#url="http://writing.upenn.edu/pennsound/x/Yau.php"

driver.get(url) #This does the magic. Loads everything.
page_html=driver.page_source


starting_url=driver.current_url
home_handle=driver.current_window_handle


nodes = driver.find_elements_by_xpath('//*')

print(len(nodes))

new_urls=[]


for i in range(len(nodes)):
    print(i)
    nodes = driver.find_elements_by_xpath('//*')
    node = nodes[-i]                               ## counting backwards from the end
    try: 
        link_url=node.get_attribute('href')
        if link_url!=None:
            new_urls.append(link_url)
    except: print("oops")
    try:
        node.click()
    except: print("oops")
    updated_nodes = driver.find_elements_by_xpath('//*')
    new_nodes=list(set(updated_nodes)-set(nodes))     ## If new nodes appear following
    for new_node in new_nodes:                        ## click, we check them for href
        try:                                          ## links but don't click the nodes.
            link_url=new_node.get_attribute('href')
            if link_url!=None:
                new_urls.append(link_url)
        except: pass
    if driver.current_url!=starting_url:
        print(driver.current_url)
        new_urls.append(driver.current_url)
        driver.back()
        driver.switch_to_window(home_handle)
    print(driver.current_url)
    time.sleep((0.1*random.random()))
    i+=1


for item in sorted(list(set(new_urls))):
    print(item)







