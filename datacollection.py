import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
import json
from bs4 import BeautifulSoup as BS
import csv



chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('driver/chromedriver',chrome_options=chrome_options)

desired_cap = chrome_options.to_capabilities()


base_url_g = u'https://google.com/search?q='
youtube_base_url = 'https://youtube.com/'

def y_search_bot(query):
    '''
    This helper function takes in a query and searches for that query on YouTube using Selenium. 
    '''
    
    driver.get(youtube_base_url)
    sleep(5)
    
    query_box = driver.find_element_by_xpath('/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input')
    query_box.send_keys(query)
    
    sleep(5)
    
    search_icon = driver.find_element_by_xpath('/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/button')
    search_icon.click()

    
def y_get_results():
    '''
    This helper function collects the titles of the results on the YouTube SERP and returns all the titles in a list. 
    '''

    #result_links = []
    
    #soup = BS(driver.page_source, 'html.parser')
    #search = soup.find_all('div', class_="text-wrapper style-scope ytd-video-renderer")
    #for h in search:
        #result_links.append(h.div.div.h3.a.get('title'))
        
    return driver.page_source

def search_and_get_results(query):

    '''
    Combines y_search_bot and y_get_results to search and collect results from YouTube.
    '''
    y_search_bot(query)
    sleep(5)

    result_html = y_get_results()

    sleep(5)

    with open('SERP/{}.html'.format(query), 'w') as result_file:
        json.dump(result_html, result_file)

with open('queries.csv', 'r') as inputF:
    queries = []
    reader = csv.reader(inputF)
    for row in reader:
        queries.append(row[0])

for query in queries:
    '''
    Goes through the list of queries and searches for each query on YouTube. 
    '''
    search_and_get_results(query)
driver.close()
