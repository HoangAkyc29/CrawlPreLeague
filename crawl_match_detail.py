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
    file_path = os.path.join('url_match_data', filename)

    # Đọc dữ liệu từ file txt và lấy phần tử cuối cùng của mỗi dòng
    with open(file_path, 'r') as f:
        for line in f:
            data = line.strip().split('_')[-1]
            data_list.append(data)

    #print(data_list)

    url = 'https://www.soccer24.com/match/CWuae5l9/#/match-summary/match/'

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

for filename in txt_files:
    #mỗi filename tương ứng với 1 season.
    urlmatchlist = Get_urlmatch_list(filename)

    #sử dụng các url này để lấy dữ liệu từng match
    for url in urlmatchlist:
        driver = webdriver.Chrome()
        driver.get(url)

        #code crawl dữ liệu của match ở đây

        time.sleep(2)
        driver.quit()

    #crawl được match detail rồi thì ghép dữ liệu vào file excel với match trong mùa giải đó tương ứng
    #sau đó đưa ra kết quả cuối cùng vào final_result_data.

