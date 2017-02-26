from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
from lxml import html 
from selenium import webdriver
import random
import time
#from bs4 import BeautifulSoup


url="https://statesummaries.ncics.org"   ## Set URL for page to be analyzed.


driver = webdriver.PhantomJS()  ## Initializing headless browser.
driver.get(url)                 ## Loads page in browser.
page_source=driver.page_source  ## Assigns page source to a variable (helpful for analyzing static pages containing elements rendered by JavaScript, though not used below.)

starting_url=driver.current_url               ## Gets current URL in format used by Selenium.
home_handle=driver.current_window_handle      ## Gets ID for current browser window.

nodes = driver.find_elements_by_xpath('//*')  ## Gets list of all nodes in DOM.
print(len(nodes))                             ## Prints number of nodes for reference.

new_urls=[]                     ## Our master list of link URLs

page_changed = False

for i in range(len(nodes)):
    print(i)
    if page_changed == True:
        nodes = driver.find_elements_by_xpath('//*')   ## Gets list of all nodes in DOM. Doing this every time we navigate away from starting page or alter the DOM. Assumes nodes and order remain identical throughout (i.e., that the starting page doesn't change over the course of analysis).
        page_changed = False
    node = nodes[i]                                ## Node we'll be working with in this step.
    try: 
        link_url=node.get_attribute('href')        ## Grabs href link if present
        if link_url!=None:
            new_urls.append(link_url)
    except: pass                                   ## Ignoring errors here and below 
    try:
        node.click()                               ## Clicks on node in browser
    except: pass                                   ## Clicking an invisible node throws an error.
    if driver.current_url!=starting_url:           ## If click leads to new URL,
        print(driver.current_url)                  ## print it,
        new_urls.append(driver.current_url)        ## add to URL list,
        driver.back()                              ## and navigate back to starting page.
        driver.switch_to_window(home_handle)       ## Just in case page loaded in new window.
        page_changed = True
    else:                                                      ## If click doesn't lead to new URL,
        updated_nodes = driver.find_elements_by_xpath('//*')   ## get list of nodes in current DOM. 
        new_nodes=list(set(updated_nodes)-set(nodes))          ## Identify list of newly created nodes.
        if len(new_nodes)>0:
            page_changed = True
        for new_node in new_nodes:
            try:                                               ## For each new node,
                link_url=new_node.get_attribute('href')        ## check for href links and add to URL list.
                if link_url!=None:
                    new_urls.append(link_url)                  ## Unlike master node list, we don't click on the newly created nodes.
            except: pass
    print(driver.current_url)           ## Feedback to confirm we're still on the page we started with.
    time.sleep((0.1*random.random()))   ## Random sleep between 0 and 0.1 seconds to avoid overloading server.
    i+=1

new_urls = sorted(list(set(new_urls)))  ## Removes duplicate links and alphabetizes list

for item in new_urls:                   ## Prints final link list
    print(item)





