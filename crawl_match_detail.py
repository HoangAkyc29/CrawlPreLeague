from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd
import requests

chrome_options = Options()
chrome_options.add_argument('--headless')

#filename = 'premier-league-2021-2022.txt'

result_dir = 'url_match_data'

# Lấy danh sách tên file trong thư mục 'url_match_data'
file_list = os.listdir(result_dir)

# Lọc ra danh sách các file có đuôi là .txt
txt_files = [f for f in file_list if f.endswith('.txt')]

# In danh sách các file .txt
#print(txt_files)

def Get_urlmatch_list(string_txt):

    data_list = []

    # Xác định đường dẫn tới file txt
    file_path = os.path.join('url_match_data', string_txt)

    # Đọc dữ liệu từ file txt và lấy phần tử cuối cùng của mỗi dòng
    with open(file_path, 'r') as f:
        for line in f:
            data = line.strip().split('_')[-1]
            data_list.append(data)

    #print(data_list)

    url = 'https://www.soccer24.com/match/CWuae5l9/#/match-summary/match-statistics/'

    url_list = []

    # Lặp qua các sample data
    for data in data_list:
        # Tách giá trị cuối cùng của data phân cách bởi dấu '_'
        match_id = data.split('_')[-1]

        # Tạo url mới bằng cách thay thế giá trị chỗ 'CWuae5l9' bằng match_id
        new_url = url.replace('CWuae5l9', match_id)

        # Append url mới vào url_list
        url_list.append(new_url)

    print(url_list)
    return url_list

def GetSelectedData(original_list):
    return original_list[:5] + original_list[-8:]

def GetCategory():
    url_test = 'https://www.soccer24.com/match/CWuae5l9/#/match-summary/match-statistics/'
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_test)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    category_values = []
    category_divs = soup.find_all('div', {'class': 'stat__categoryName'})
    for category_div in category_divs:
        value = category_div.text.strip()
        category_values.append(value)

    print(GetSelectedData(category_values))

    category_excel = []

    for item in GetSelectedData(category_values):
        category_excel.append(item + "__Home")
        category_excel.append(item + "__Away")

    category_bouns = ['Team Home', 'Team Away', 'Score Home', 'Score Away']
    category_excel = category_bouns + category_excel

    print(category_excel)
    driver.quit()

    return category_excel

GetCategory()
count = 0


for filename in txt_files:
    #mỗi filename tương ứng với 1 season.
    urlmatchlist = Get_urlmatch_list(filename)
    data_list = []

    #sử dụng các url này để lấy dữ liệu từng match trong season đó
    for url in urlmatchlist:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Tìm các thẻ span trong div detailScore__wrapper và lấy ra giá trị text
        span_tags = soup.select_one('div.detailScore__wrapper').find_all('span')
        text_values = [tag.text for tag in span_tags]
        text_values.pop(1)
        # print(text_values)

        team_name_values = []
        team_name_divs = soup.find_all('div', {'class': 'participant__participantName'})
        for team_name_div in team_name_divs:
            value = team_name_div.text.strip()
            team_name_values.append(value)

        # print(team_name_values)

        stat_home_values = []
        stat_home_divs = soup.find_all('div', {'class': 'stat__homeValue'})
        for stat_home_div in stat_home_divs:
            value = stat_home_div.text.strip()
            stat_home_values.append(value)

        print(GetSelectedData(stat_home_values))

        stat_away_values = []
        stat_away_divs = soup.find_all('div', {'class': 'stat__awayValue'})
        for stat_away_div in stat_away_divs:
            value = stat_away_div.text.strip()
            stat_away_values.append(value)

        print(GetSelectedData(stat_away_values))

        final_value_data = []
        final_value_data = team_name_values + text_values

        for i in range(len(GetSelectedData(stat_home_values))):
            final_value_data.append(GetSelectedData(stat_home_values)[i])
            final_value_data.append(GetSelectedData(stat_away_values)[i])

        print(final_value_data)
        data_list.append(final_value_data)
        driver.quit()
        #break
    #---------------------------------------------------------------

    # Tạo thư mục nếu chưa tồn tại
    dir_name = 'final_result_data'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    # Tạo DataFrame từ list và lưu vào file excel
    df = pd.DataFrame(data_list, columns=GetCategory())
    df['Score Home'] = pd.to_numeric(df['Score Home'], errors='coerce')
    df['Score Away'] = pd.to_numeric(df['Score Away'], errors='coerce')
    file_name_xml = filename + '.xlsx'  # Tên file được lấy từ url ban đầu
    file_path = os.path.join(dir_name, file_name_xml)
    df.to_excel(file_path, index=False)
    #break

#------------------------------------------------------------------------------------------------

# url_test = 'https://www.soccer24.com/match/CWuae5l9/#/match-summary/match-statistics/'
#
# driver = webdriver.Chrome(options=chrome_options)
# driver.get(url_test)
# soup = BeautifulSoup(driver.page_source, 'html.parser')
#
# # Tìm các thẻ span trong div detailScore__wrapper và lấy ra giá trị text
# span_tags = soup.select_one('div.detailScore__wrapper').find_all('span')
# text_values = [tag.text for tag in span_tags]
# text_values.pop(1)
# #print(text_values)
#
# team_name_values = []
# team_name_divs = soup.find_all('div', {'class': 'participant__participantName'})
# for team_name_div in team_name_divs:
#     value = team_name_div.text.strip()
#     team_name_values.append(value)
#
# #print(team_name_values)
#
# stat_home_values = []
# stat_home_divs = soup.find_all('div', {'class': 'stat__homeValue'})
# for stat_home_div in stat_home_divs:
#     value = stat_home_div.text.strip()
#     stat_home_values.append(value)
#
# print(GetSelectedData(stat_home_values))
#
# stat_away_values = []
# stat_away_divs = soup.find_all('div', {'class': 'stat__awayValue'})
# for stat_away_div in stat_away_divs:
#     value = stat_away_div.text.strip()
#     stat_away_values.append(value)
#
# print(GetSelectedData(stat_away_values))
#
# final_value_data = []
# final_value_data = team_name_values + text_values
#
# for i in range(len(GetSelectedData(stat_home_values))):
#     final_value_data.append(GetSelectedData(stat_home_values)[i])
#     final_value_data.append(GetSelectedData(stat_away_values)[i])
#
# print(final_value_data)
#
# driver.quit()