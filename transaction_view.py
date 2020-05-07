from selenium import webdriver
from bs4 import BeautifulSoup
import re
import datetime

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('C:/webdriver/chromedriver.exe', chrome_options=options)

#driver = webdriver.Chrome('C:/webdriver/chromedriver.exe')

print('TxID를 입력해주세요')
txid = input()
if txid == "":
    txid = '0xe78e8d64a4fffd56defd40021238f80e3d4135d13508f0dbe73875343c419bb8' # default TxID

driver.get('https://explorer.orbitchain.kr/transactions/' + txid)

try:
    driver.find_element_by_css_selector('.tab-btn').click()
except:
    print('입력하신 트랜잭션을 찾을 수 없습니다.')

orbit_title_list = []
orbit_text_list = []
orbit_list = []
orbit_event_name_temp_ticket = 0 # Event Name일 시 1, Event Name이 아닐 시 0
orbit_event_kor = {'Liquidate Market Change' : '청산마켓 변동', 'Liquidate Borrow' : '대차 상환',
                   'Market Change' : '마켓 변동', 'Liquidate Supply' : '청산 공급',
                   'Pool Withdraw' : '컨트랙트 Pool에서 출금', 'Transfer' : '전송', 'Balance Change' : '잔액 변동',
                   'Liquidate Trade' : '청산마켓 거래', 'Pool Supply' : '컨트랙트 Pool에 공급'}

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
first_title = True
try:
    for orbit_list_details in orbit_list:
        # print(orbit_list_details)

        # if orbit_list_details[0] == 'Event Name':
        #    print(orbit_list_details[1])
        title = orbit_list_details[0]
        detail = orbit_list_details[1]

        if title == 'Event Name' and first_title == True:
            try:
                print(orbit_event_kor[detail])
                first_title = False
            except:
                print(detail)
                first_title = False

        elif title == 'Event Name' and first_title == False:
            try:
                print()
                print(orbit_event_kor[detail])
            except:
                print()
                print(detail)

        elif title == 'Token Id':
            token_name = re.search('(\S+)', detail).group()
            token_address_remove = token_name.replace(token_name + " ", "")
            token_address = detail.replace(token_address_remove + " ", "")
            token_name = token_name[1: (len(token_name) - 1)]
            print("Token : " + token_name)
            print("Addr : " + token_address)

        elif any(['Amount' in title, 'Total Supply' in title, 'Borrow' in title, 'Total Withdraw' in title]):
            amount = float(detail) * 0.00000001
            print(title + " " + '{:,.8f}'.format(amount))

        elif 'Time' in title:
            dt_obj_timestamp = int(detail)
            dt_obj = datetime.datetime.fromtimestamp(dt_obj_timestamp)
            print(title + " " + dt_obj.strftime('%Y-%m-%d %H:%M:%S'))

        elif 'Is Force' in title:
            title = '청산종류'
            if detail == 'false':
                detail = '자율청산'
            elif detail == 'true':
                detail = '강제청산'
            print(title + " " + detail)

        elif 'Is Withdraw' in title:
            title = '출금여부'
            if detail == 'false':
                detail = 'X'
            elif detail == 'true':
                detail = 'O'
            print(title + " " + detail)

        else:
            print(title + " " + detail)

except Exception as e:
    print(e)
    pass
driver.quit()
