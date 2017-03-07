#!/usr/bin/env python3

import logging
import argparse
import random
import time
from lxml import html
from selenium import webdriver
from interfaceutils import ProgressBar
from interfaceutils import UniqueFileWrite

# User-editable options

inputurl = "https://statesummaries.ncics.org/co" # The URL to be analyzed
outfileName = "urls.txt"      # The file to output the resulting URLs to

################################################################################
### Users: do not edit below this line unless you know what you're doing! ######
################################################################################

logger = logging.getLogger(__name__)

def get_links_from_url(url, outfile, displayProgress=False):
    """
    Get all links that are accessible from the given webpage.

    Given the string url, gets a list of all links accessible. Attempts to
    emulate a human sitting in front of a browser as much as possible:
    will click on things to see if they edit the DOM (dynamic generation).

    Does not yet support hover, infinite scroll, or dropdown menus.

    url (string): the URL to crawl
    outfile (file handle): the file to store the output URLs in. NOTE: NOT A NAME
    displayProgress (bool): whether progress should be displayed on STDOUT

    """

    if displayProgress:
        print("Setting up web drivers. This can take a few seconds...\n")

    ### Set up web crawling structures and classes

    driver = webdriver.PhantomJS()  # Initializing headless browser.
    driver.get(url)                 # Loads page in browser.
    page_source = driver.page_source  # helpful for analyzing static pages
                                    # containing elements rendered by
                                    # JavaScript, though not used below.

    starting_url = driver.current_url
    home_handle = driver.current_window_handle

    nodes = driver.find_elements_by_xpath('//*')  ## Gets list of all nodes in DOM.
    logger.info("For URL %s, I initially found %d nodes in the DOM",
                starting_url, len(nodes))

    new_urls = list()         # Running list of identified links
    dom_changed = False

    # Check to see if someone passed a string instead of a file and take care of
    # putting header information in at the same time
    try:
        outfile.write("URL List scraped from " + url  + "\n\n")
    except:
        print("[ERR]: get_links_from_url was passed a bad file handle.")
        print("A programmer somewhere dun goofed!")
        logger.error("I was given a non-file for outfile! The file should" +
                     "be created, e.g., with a call to open()")
        return

    fileWriter = UniqueFileWrite(outfile)

    ### Crawling structure initialized

    # Set up interfaces for our users
    if displayProgress:
        print("\n == I'm going to begin juicing links now == ")
        print("""\nPlease note that new links may be discovered as progress
is made, so the progress bar may actually grow longer
while the procedure is running. Please be patient!\n""")
        progressBar = ProgressBar(len(nodes), fmt=ProgressBar.FULL)

    for node in nodes:
        if dom_changed:
            # Gets list of all nodes in DOM. Doing this every time we navigate
            # away from starting page or alter the DOM. Assumes nodes and order
            # remain identical throughout (i.e., that the starting page doesn't
            # change over the course of analysis).

            # NOTE: This is a seriously dicey assumption and should probably be
            # fixed in future versions
            nodes = driver.find_elements_by_xpath('//*')
            page_changed = False
        try:
            link_url = node.get_attribute('href')   # Grabs href link if present
            if link_url is not None:
                new_urls.append(link_url)
        except:
            logger.exception("Got exception while attempting to process %s",
                             str(node))
        try:
            node.click()                     ## Clicks on node in browser
        except:
            logger.exception("Got exception while attempting to click on %s",
                             str(node))

        # If the click led to a new URL, update the info accordingly
        if driver.current_url != starting_url:
            logger.info("New URL found: %s", driver.current_url)
            new_urls.append(driver.current_url)

            # Navigate back to the homepage and switch to the original handle
            # in case the link opened in a new window
            driver.back()
            driver.switch_to_window(home_handle)
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
        if driver.current_url != url:
            logging.warning("The driver has somehow left its home url. The\
                             correct url is %s, while its currently on %s.",
                             url, driver.current_url)
        time.sleep((0.1*random.random()))  # We want to avoid DOSing the server, sleep a bit

        # Update our progress
        if displayProgress:
            progressBar.current += 1
            progressBar.total = len(nodes)
            progressBar()

        # Use UniqueFileWrite to update the file with URLs not currently in the file
        fileWriter.update_file_and_flush(new_urls)

    if displayProgress:
        progressBar.done()

if __name__ == "__main__":
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    with open(outfileName,'w') as outF:
        get_links_from_url(inputurl, outF, displayProgress=True)
