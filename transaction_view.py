import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re

driver = webdriver.Chrome('C:/webdriver/chromedriver.exe')
driver.get('https://explorer.orbitchain.kr/transactions/0xe78e8d64a4fffd56defd40021238f80e3d4135d13508f0dbe73875343c419bb8')
driver.find_element_by_css_selector('.tab-btn').click()

orbit_title_list = []
orbit_text_list = []
orbit_list = []
orbit_event_name_temp_ticket = 0 # Event Name일 시 1, Event Name이 아닐 시 0
orbit_event_kor = {'Liquidate Market Change' : '청산마켓 변동', 'Liquidate Borrow' : '대차 상환',
                   'Market Change' : '마켓 변동', 'Liquidate Supply' : '청산 공급'}

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

event = soup.select('#transactionDetail > article > div.detail > div > div.event-div > div > p')
event_html = soup.select('#transactionDetail > article > div.detail > div > div.event-div > div')

for event_elements in event_html:
    for event_details in event_elements:
        event_title = event_details.select('span.title')

        for event_title_details in event_title:
            orbit_title_list.append(event_title_details.text)

        event_text = event_details.select('span.text')
        for event_text_details in event_text:
            orbit_text_list.append(event_text_details.text)

try:
    for details_no in range(0, len(orbit_title_list)):
        if 'Event Name' in orbit_title_list[details_no]:
            orbit_event_name_temp = orbit_text_list[details_no]
            orbit_event_name_temp_ticket = 1

        if orbit_event_name_temp_ticket == 1 and orbit_title_list[details_no].find('Event Name') == -1:
            orbit_event_name_temp = orbit_event_name_temp.strip()
            orbit_list.append(['Event Name', orbit_event_name_temp])
            orbit_event_name_temp_ticket = 0

        if orbit_event_name_temp_ticket == 0 and orbit_title_list[details_no].find('Event Name') == -1:
            orbit_list.append([orbit_title_list[details_no], orbit_text_list[details_no]])

        # orbit_list.append([orbit_title_list[details_no], orbit_text_list[details_no]])
except:
    pass
try:
    for orbit_list_details in orbit_list:
        # print(orbit_list_details)

        # if orbit_list_details[0] == 'Event Name':
        #    print(orbit_list_details[1])
        if orbit_list_details[0] == 'Event Name':
            try:
                print(orbit_event_kor[orbit_list_details[1]])
            except:
                print(orbit_list_details[1])

        elif orbit_list_details[0] == 'Token Id':
            token_name = re.search('(\S+)', orbit_list_details[1]).group()
            token_address_remove = token_name.replace(token_name + " ", "")
            token_address = orbit_list_details[1].replace(token_address_remove + " ", "")
            token_name = token_name[1: (len(token_name) - 1)]
            print("Token : " + token_name)
            print("Addr : " + token_address)

        elif 'Amount' in orbit_list_details[0]:
            amount = float(orbit_list_details[1]) * 0.00000001
            print(orbit_list_details[0] + " " + '%.8f' % amount)

        else:
            print(orbit_list_details[0] + " " + orbit_list_details[1])

except:
    pass

input()
driver.quit()
