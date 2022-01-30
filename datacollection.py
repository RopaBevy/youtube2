import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
import json
from bs4 import BeautifulSoup as BS



chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('driver/chromedriver',chrome_options=chrome_options)
# chrome_options.add_experimental_option("prefs", { "profile.default_content_settings.geolocation": 1})
# chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# chrome_driver_binary = "/usr/local/bin/chromedriver"
desired_cap = chrome_options.to_capabilities()

# driverpath ='driver/chromedriver'
# driver = webdriver.Chrome(executable_path=driverpath, chrome_options=chrome_options)

base_url_g = u'https://google.com/search?q='
youtube_base_url = 'https://youtube.com/'

def y_search_bot(query):
    
    driver.get(youtube_base_url)
    sleep(5)
    
    query_box = driver.find_element_by_xpath('/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input')
    query_box.send_keys(query)
    
    sleep(5)
    
    search_icon = driver.find_element_by_xpath('/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/button')
    search_icon.click()

    
def y_get_results():
    result_links = []
    
    soup = BS(driver.page_source, 'html.parser')
    search = soup.find_all('div', class_="text-wrapper style-scope ytd-video-renderer")
    for h in search:
        result_links.append(h.div.div.h3.a.get('title'))
        
    return result_links

def search_and_get_results(query):
    y_search_bot(query)
    sleep(5)

    results_dict = y_get_results()

    sleep(5)

    with open('youtube_results'+query, 'w') as result_file:
        json.dump(results_dict, result_file)


queries = ['adele', 'khalid', 'ropafadzo beverly shava']

for query in queries:
    search_and_get_results(query)
driver.close()
