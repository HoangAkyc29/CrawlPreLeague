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
import pandas as pd
import requests

chrome_options = Options()
chrome_options.add_argument('--headless')

#đây là đoạn code lấy ra url của các trận đấu bóng đá từ trang https://www.premierleague.com/results từ mùa giải 2006 - 2023


#hàm lấy ra url của các trận đấu bóng đá trong 1 mùa giải xác định
def Geturlmatchperseason(season) :
    # Khởi tạo trình duyệt và mở trang web
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.premierleague.com/results")

    # Chờ trang web load xong
    driver.implicitly_wait(5)

    # Đợi cho element của cookie xuất hiện và click vào nút accept
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))
        )
        accept_button.click()
    except:
        # Nếu không tìm thấy element của cookie hoặc không thể click được, bỏ qua
        pass

    time.sleep(5)
    #------------------------------------------------------------------------------------------------

    # Chờ cho dropdown xuất hiện và lấy đối tượng dropdown
    wait = WebDriverWait(driver, 5)
    dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-dropdown-current="comps"]')))

    # Click vào dropdown để mở ra danh sách option
    dropdown.click()

    # Lấy danh sách các option
    options = dropdown.find_element(By.XPATH,'../ul[@data-dropdown-list="comps"]')

    # Tìm và click vào option mong muốn có data-option-name="2021/22"
    for option in options.find_elements(By.TAG_NAME,'li'):
        if option.get_attribute('data-option-name') == 'Premier League':
            option.click()
            break

    #------------------------------------------------------------------------------------------------
    # Chờ cho dropdown xuất hiện và lấy đối tượng dropdown
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-dropdown-current="compSeasons"]')))

    # Click vào dropdown để mở ra danh sách option
    dropdown.click()

    # Lấy danh sách các option
    options = dropdown.find_element(By.XPATH,'../ul[@data-dropdown-list="compSeasons"]')

    # Tìm và click vào option mong muốn có data-option-name="2021/22"
    for option in options.find_elements(By.TAG_NAME,'li'):
        if option.get_attribute('data-option-name') == season:
            option.click()
            break

    time.sleep(3)
    #------------------------------------------------------------------------------------------------

    # Lặp lại việc lăn chuột xuống dưới cho đến khi không còn có thêm dữ liệu mới
    for _ in range(5):
        # Lăn chuột xuống dưới
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Chờ 2 giây để cho trang web tải thêm dữ liệu
        time.sleep(2)

    # Tìm tất cả các thẻ div có class="fixture postMatch" và lấy ra tất cả data-href của chúng
    post_match_divs = driver.find_elements(By.CSS_SELECTOR,'div.fixture.postMatch')
    data_hrefs = [div.get_attribute('data-href') for div in post_match_divs]

    # Đóng trình duyệt
    driver.quit()

    # In danh sách các data-href
    print(data_hrefs)

    return data_hrefs

season_sample = "2022/23"
season_list = []
for year in range(2006, 2023):
    season = str(year) + "/" + str(year+1)[2:]
    season_list.append(season)

print(season_list)

for theseason in season_list:
    url_match_data = Geturlmatchperseason(theseason)
    #url_match_data là danh sách url của tất cả trận đấu trong mùa giải 'theseason'
    new_season_string = theseason.replace("/", " to ")

    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists('url_match_data_official'):
        os.makedirs('url_match_data_official')

    # Tạo đường dẫn đầy đủ của file
    file_path = os.path.join('url_match_data_official', new_season_string +'.txt')

    # ---------------------------------------------------------------------------------------
    # Lưu danh sách ID vào file trong thư mục url_match_data

    # Xóa file nếu đã tồn tại
    if os.path.exists(file_path):
        os.remove(file_path)

    #lưu url_match_data vào file txt trong url_match_data_official
    
    with open(file_path, 'w') as f:
        for element in url_match_data:
            f.write(element + '\n')
