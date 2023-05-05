from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import pandas as pd
import requests

#url = 'https://www.soccer24.com/england/premier-league-2021-2022/results/'
baseurl = 'https://www.soccer24.com/england/premier-league-{year1}-{year2}/results/'

url_season_list = []
for i in range(20):
    year1 = 2021 - i
    year2 = 2022 - i
    url = baseurl.format(year1=year1, year2=year2)
    url_season_list.append(url)

print(url_season_list)

def GetDataperSeason(url):
    driver = webdriver.Chrome()
    driver.get(url)

    # Tìm nút theo tên class và bấm nó
    #button = driver.find_element(By.CLASS_NAME, 'event__more')
    while True:
        try:
            xpath = "//a[contains(text(),'Show more matches')]"
            show_more_button = driver.find_element("xpath", xpath)
            driver.execute_script("arguments[0].scrollIntoView();", show_more_button)  # Scroll đến vị trí của nút
            time.sleep(1)  # Đợi 1 giây để tránh lỗi do trang web load chậm
            actions = ActionChains(driver)
            actions.move_to_element(show_more_button).click().perform()  # Nhấn nút
            time.sleep(1)  # Đợi 1 giây trước khi thực hiện các thao tác tiếp theo
        except:
            break;


    soup = BeautifulSoup(driver.page_source, 'html.parser')
    div = soup.find('div', {'class': 'leagues--static event--leagues results'})
    div_children = div.find_all('div')
    data = ''
    string_sample = ''
    setdata = []
    for i, child in enumerate(div_children):
        if child.has_attr('class') and 'event__round' in child['class']:
            continue
        if child.has_attr('class') and 'event__time' in child['class']:
            setdata.append(string_sample)
            print(string_sample)
            string_sample = ''
        data = child.text
        string_sample += data
        string_sample += " @@ "

        if i == len(div_children) - 1:
            setdata.append(string_sample)
            print(string_sample)
            string_sample = ''
        #print(data, end='')
        #print(" @@ ", end = '')

    setdata.pop(0)
    print("\n\n")

    id_list = []

    elements = driver.find_elements(By.CLASS_NAME, "event__match")
    for element in elements:
        element_id = element.get_attribute("id")
        id_list.append(element_id)

    url_parts = url.split('/')
    filename = url_parts[-3] + '.txt'

    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists('url_match_data'):
        os.makedirs('url_match_data')

    # Tạo đường dẫn đầy đủ của file
    file_path = os.path.join('url_match_data', filename)

    #---------------------------------------------------------------------------------------
    # Lưu danh sách ID vào file trong thư mục url_match_data

    # Xóa file nếu đã tồn tại
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        for element in id_list:
            f.write(element + '\n')

    #---------------------------------------------------------------------------------------
    # Lưu kết quả các trận đấu của mùa giải vào file trong thư mục result_data

    # Tạo thư mục nếu chưa tồn tại
    dir_name = 'result_data'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    # Tách giá trị trong các chuỗi và lưu vào list
    data_list = []
    for data in setdata:
        values = data.split('@@')[:5]
        data_list.append(values)

    # Tạo DataFrame từ list và lưu vào file excel
    df = pd.DataFrame(data_list, columns=['Time', 'Home', 'Away', 'Score Home', 'Score Away'])
    df['Score Home'] = pd.to_numeric(df['Score Home'], errors='coerce')
    df['Score Away'] = pd.to_numeric(df['Score Away'], errors='coerce')
    file_name_xml = filename + '.xlsx' # Tên file được lấy từ url ban đầu
    file_path = os.path.join(dir_name, file_name_xml)
    df.to_excel(file_path, index=False)

    driver.quit()

for urlseason in url_season_list:
    GetDataperSeason(urlseason)


