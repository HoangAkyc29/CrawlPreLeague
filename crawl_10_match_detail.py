from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import os
import re
import pandas as pd
import requests

#----------------------------------------------------------------------------------------------
def Get_urlmatch_list(string_filename_txt):
    # Xác định đường dẫn tới file txt
    file_path = os.path.join('url_match_data_official', string_filename_txt)
    # Đọc dữ liệu từ file txt và lấy phần tử cuối cùng của mỗi dòng
    data_list = []
    with open(file_path, 'r') as f:
        for line in f:
            data_list.append("https:" + line.strip())

    return data_list
def GetCategory():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.premierleague.com/match/5937")
    # Đợi cho element của cookie xuất hiện và click vào nút accept
    try:
        accept_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))
        )
        accept_button.click()
    except:
        # Nếu không tìm thấy element của cookie hoặc không thể click được, bỏ qua
        pass

    time.sleep(2)
    li_element = driver.find_element(By.CSS_SELECTOR, "li[data-tab-index='2']")
    li_element.click()

    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tbody = soup.find('tbody', {'class': 'matchCentreStatsContainer'})
    p_children = tbody.find_all('p')
    matchdata = []
    for child in p_children:
        matchdata.append(child.text)

    # In kết quả
    # print(p_children)
    print(matchdata)

    list2 = [matchdata[i] for i in range(len(matchdata)) if i % 3 == 1]
    print(list2)

    category_excel = []

    for item in list2:
        category_excel.append(item + "__Home")
        category_excel.append(item + "__Away")

    category_bouns = ['Team Home', 'Team Away', 'Score Home', 'Score Away']
    category_excel = category_bouns + category_excel

    print(category_excel)
    driver.quit()
    return category_excel

#----------------------------------------------------------------------------------------------

#GetCategory()

#----------------------------------------------------------------------------------------------

# Tìm element và bấm
driver = webdriver.Chrome()
# Đặt kích thước của cửa sổ trình duyệt
driver.set_window_size(400, 300)

# Đặt vị trí của cửa sổ trình duyệt
driver.set_window_position(0, 0)

def MatchDetailData(url):
    # # Tìm element và bấm
    # driver = webdriver.Chrome()
    # # Đặt kích thước của cửa sổ trình duyệt
    # driver.set_window_size(400, 300)
    #
    # # Đặt vị trí của cửa sổ trình duyệt
    # driver.set_window_position(0, 0)
    driver.get(url)

    # Đợi cho element của cookie xuất hiện và click vào nút accept
    try:
        accept_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))
        )
        accept_button.click()
    except:
        # Nếu không tìm thấy element của cookie hoặc không thể click được, bỏ qua
        pass

    time.sleep(2)
    li_element = driver.find_element(By.CSS_SELECTOR,"li[data-tab-index='2']")
    li_element.click()

    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tbody = soup.find('tbody', {'class': 'matchCentreStatsContainer'})
    p_children = tbody.find_all('p')
    matchdata = []
    for child in p_children:
        matchdata.append(child.text)

    # In kết quả
    #print(p_children)
    print(matchdata)

    list1 = [matchdata[i] for i in range(len(matchdata)) if i % 3 == 0]
    #list2 = [matchdata[i] for i in range(len(matchdata)) if i % 3 == 1]
    list3 = [matchdata[i] for i in range(len(matchdata)) if i % 3 == 2]

    #print(list1)
    #print(list2)
    #print(list3)

    #-----------------------------------------------------------------------------------------

    resultdiv = soup.find('div', {'class': 'score fullTime'})

    score_text = resultdiv.text.strip()  # lấy nội dung của thẻ div và xóa các ký tự trắng ở đầu và cuối
    scores = re.findall('\d+', score_text)  # sử dụng regular expression để tìm các giá trị số trong nội dung
    #print(scores)
    list1.insert(0,scores[0])
    list3.insert(0,scores[1])
    #-----------------------------------------------------------------------------------------

    home_team_div = soup.find('div', {'class': 'team home'})
    home_team_long_span = home_team_div.find('span', {'class': 'long'})

    home_team_name = home_team_long_span.text

    #print(home_team_name)
    list1.insert(0,home_team_name)

    away_team_div = soup.find('div', {'class': 'team away'})
    away_team_long_span = away_team_div.find('span', {'class': 'long'})

    away_team_name = away_team_long_span.text

    #print(away_team_name)
    list3.insert(0,away_team_name)

    #-----------------------------------------------------------------------------------------
    result = []

    for a, b in zip(list1, list3):
        result.append(a)
        result.append(b)

    print(result)
    # Đóng trình duyệt

    return result

filename = "2022 to 23.txt"
Seasondata = []
for url in Get_urlmatch_list(filename):
    try:
        matchdata = MatchDetailData(url)
    except:
        continue
    print(len(matchdata))
    if(len(matchdata) == 26):
        Seasondata.append(matchdata)
    if(len(Seasondata) == 10):
        break

# Tạo thư mục nếu chưa tồn tại
dir_name = '10_match_crawl_official'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

try:
    # Tạo DataFrame từ list và lưu vào file excel
    df = pd.DataFrame(Seasondata, columns=GetCategory())
    df['Score Home'] = pd.to_numeric(df['Score Home'], errors='coerce')
    df['Score Away'] = pd.to_numeric(df['Score Away'], errors='coerce')
    newfilename = filename.split('.')[0]
    file_name_xml = newfilename + '.xlsx'  # Tên file được lấy từ url ban đầu
    file_path = os.path.join(dir_name, file_name_xml)
    df.to_excel(file_path, index=False)

    # folder_path = 'url_match_data_official'
    # file_path = os.path.join(folder_path, filename + '.txt')
    #
    # if os.path.exists(file_path):
    #     os.remove(file_path)
    #     print("File removed successfully. File remove:" + file_path)
    # else:
    #     print("File not found.")
except:
    pass

driver.quit()