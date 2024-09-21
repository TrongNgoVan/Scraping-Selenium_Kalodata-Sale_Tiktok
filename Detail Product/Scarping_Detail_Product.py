import pickle
import csv
import random
import pandas as pd

from selenium.common.exceptions import ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# Đường dẫn đến msedgedriver
edge_driver_path = "B:\\Documents\\DataScience Research(09 2024)\\edgedriver_win64\\msedgedriver.exe"

# Khởi tạo trình duyệt Edge
service = Service(executable_path=edge_driver_path)
browser = webdriver.Edge(service=service)

browser.get("https://www.kalodata.com/product/detail?id=1729577314986658654&language=vi-VN&currency=VND&region=VN")

# 2.Load cookie from file

cookies = pickle.load(open("my_cookie.pkl","rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

# 3. Refresh the browser
browser.get("https://www.kalodata.com/product/detail?id=1729577314986658654&language=vi-VN&currency=VND&region=VN")

try:
    close_button = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ant-modal-close"))
    )
    close_button.click()
    print("Đã nhấn vào nút đóng!")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")



try:
    # Chờ đến khi phần tử '30 ngày trước' hiển thị và nhấp
    button_30_days = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'30 ngày trước')]"))
    )
    button_30_days.click()
    print("Đã nhấp vào nút '30 ngày trước'.")
    sleep(15)
except Exception as e:
    print(f"Không thể nhấp vào nút '30 ngày trước': {e}")



# Định nghĩa tên file CSV
csv_file_path = r'B:\Documents\DataScience Research(09 2024)\BTL_KHDL\Scraping-Selenium_Kalodata-Sale_Tiktok\Data\product_creator.csv'

# Tạo DataFrame với các cột định trước
columns = ['Số thứ tự', 'Nhà sáng tạo', 'Số người theo dõi', 'Doanh thu', 'Lượt bán', 'Doanh thu từ video', 'Doanh thu Live']
df = pd.DataFrame(columns=columns)

# Ghi tiêu đề cột vào file CSV
df.to_csv(csv_file_path, mode='w', header=True, index=False, encoding='utf-8-sig')

count = 1
while True:
    try:
        print("Crawl Page " + str(count))
        rows = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//tr[@class="ant-table-row ant-table-row-level-0"]'))
        )

        # Danh sách chứa các dòng dữ liệu
        data = []

        # Duyệt qua từng hàng và lấy dữ liệu
        for row in rows:
            try:
                # Cờ đánh dấu việc lấy dữ liệu thành công
                found_all_elements = True

                # Lấy số thứ tự
                try:
                    number = row.find_element(By.XPATH, './/td[@class="ant-table-cell ant-table-cell-fix-left"]').text
                except:
                    found_all_elements = False

                # Lấy tên người dùng
                try:
                    username = row.find_element(By.XPATH, './/div[contains(@class, "line-clamp-1 group-hover:text-primary")]').text
                except:
                    found_all_elements = False

                # Lấy số lượng người theo dõi
                try:
                    followers = row.find_element(By.XPATH, './/div[contains(@class, "text-base-999")]').text
                except:
                    found_all_elements = False

                # Lấy dữ liệu từ các thẻ <td> khác
                try:
                    gia_tri1 = row.find_element(By.XPATH, './/td[@class="ant-table-cell ant-table-column-sort"]').text
                    gia_tri2 = row.find_element(By.XPATH, './/td[@class="ant-table-cell"][1]').text
                    gia_tri3 = row.find_element(By.XPATH, './/td[@class="ant-table-cell"][2]').text
                    gia_tri4 = row.find_element(By.XPATH, './/td[@class="ant-table-cell"][3]').text
                except:
                    found_all_elements = False

                if found_all_elements:
                    data.append([number, username, followers, gia_tri1, gia_tri2, gia_tri3, gia_tri4])
                    print(f"Số thứ tự: {number}, Nhà sáng tạo: {username}, Số người theo dõi: {followers}")
            except Exception as e:
                print(f"Đã xảy ra lỗi: {e}")
                continue

        if data:
            df_new = pd.DataFrame(data, columns=columns)
            df_new.to_csv(csv_file_path, mode='a', header=False, index=False, encoding='utf-8-sig')
            print("Đã lưu dữ liệu trang tương ứng vào CSV!")


       

        # Click nút phân trang
        next_pagination = browser.find_element(By.XPATH, '//button[contains(@class, "ant-pagination-item-link")]//span[@aria-label="right"]')
        next_pagination.click()
        print("Clicked on button next page!")

        # Chờ ngẫu nhiên trước khi tiếp tục
        sleep(random.randint(1, 3))
        count += 1

    except ElementNotInteractableException:
        print("Element Not Interactable Exception!")
        break


browser.quit()
import pandas as pd

# Đọc tệp CSV
df = pd.read_csv('B:\Documents\PreprocessingData-main\PreprocessingData-main\PreprocessingData.csv')

# Kiểm tra tổng số dữ liệu thiếu trong mỗi cột
missing_data = df.isnull().sum()

print(missing_data)

