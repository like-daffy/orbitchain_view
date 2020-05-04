import requests
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('C:/webdriver/chromedriver.exe')
driver.get('https://explorer.orbitchain.kr/transactions/0xe78e8d64a4fffd56defd40021238f80e3d4135d13508f0dbe73875343c419bb8')
driver.find_element_by_css_selector('.tab-btn').click()

orbit_title_list = []
orbit_text_list = []

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

event = soup.select('#transactionDetail > article > div.detail > div > div.event-div > div > p')
event_html = soup.select('#transactionDetail > article > div.detail > div > div.event-div > div')
#event_contents = soup.select('#transactionDetail > article > div.detail > div > div.event-div > div > p > span.text')

for event_elements in event_html:
    for event_details in event_elements:
        event_title = event_details.select('span.title')
        #print(event_title)
        #print(event_title)
        for event_title_details in event_title:
            orbit_title_list.append(event_title_details.text)
            #print(event_title_details.text)

        event_text = event_details.select('span.text')
        for event_text_details in event_text:
            orbit_text_list.append(event_text_details.text)
            #print(event_text_details.text)
        try:
            for details_no in range(0, 10):
                print(orbit_title_list[details_no])
                print(orbit_text_list[details_no])
        except:
            pass

'''
for event_details in event_contents:
    print(event_details.text)
'''

input()
driver.quit()