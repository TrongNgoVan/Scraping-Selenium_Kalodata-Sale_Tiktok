import pickle
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

# Đường dẫn đến msedgedriver
edge_driver_path = "B:\\Documents\\DataScience Research(09 2024)\\edgedriver_win64\\msedgedriver.exe"

# Khởi tạo trình duyệt Edge
service = Service(executable_path=edge_driver_path)
browser = webdriver.Edge(service=service)

# 1. Mở trang đăng nhập
# Bước này tôi đăng nhập gián tiếp qua link này để lúc đăng nhập xong nó vào thẳng luôn đỡ qua trang chủ lại mất công tìm thẻ button để nhấn vào 
browser.get("https://www.kalodata.com/video/detail?id=7396229557373766919&language=vi-VN&currency=VND&region=VN&dateRange=%5B%222024-08-30%22%2C%222024-09-05%22%5D")

# Đợi để trang tải xong
sleep(2)

# 3. Nhập số điện thoại
try:
    phone_field = browser.find_element(By.ID, "register_phone")
    phone_field.clear()
    phone_field.send_keys("0904708498")  # Thay đổi số điện thoại nếu cần
except Exception as e:
    print(f"Không tìm thấy trường số điện thoại: {e}")

# 4. Nhập mật khẩu
try:
    password_field = browser.find_element(By.ID, "register_password")
    password_field.clear()
    password_field.send_keys("trongtiktok")  # Thay đổi mật khẩu nếu cần
except Exception as e:
    print(f"Không tìm thấy trường mật khẩu: {e}")

# 5. Nhấn vào nút đăng nhập
try:
    submit_button = browser.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Log in')]")
    submit_button.click()
    sleep(2)  # Đợi trang tải xong
except Exception as e:
    print(f"Không tìm thấy nút đăng nhập (submit): {e}")

# 6. Điều hướng đến trang shop chi tiết sau khi đăng nhập
try:
    browser.get("https://www.kalodata.com/shop/detail?id=7494529979361168222&language=vi-VN&currency=VND&region=VN")
    sleep(1)  # Đợi trang shop tải xong
except Exception as e:
    print(f"Không thể điều hướng đến trang shop: {e}")

# 7. Nhấn vào nút "Đã hiểu" để tắt thông báo
try:
    da_hieu_button = browser.find_element(By.XPATH, "//div[text()='Đã hiểu']")
    da_hieu_button.click()
    sleep(1)  # Đợi thông báo tắt

    # Chuyển sang tab mới sau khi nhấn 'Đã hiểu'
    browser.switch_to.window(browser.window_handles[-1])  # Chuyển sang tab mới (tab cuối cùng mở)
    print("Đã chuyển sang tab mới.")

    sleep(1)  # Đợi trang mới tải xong

    # Quay lại tab cũ
    browser.switch_to.window(browser.window_handles[0])  # Chuyển lại về tab đầu tiên
    print("Đã quay lại tab cũ.")
    sleep(1)
    
except Exception as e:
    print(f"Không tìm thấy nút 'Đã hiểu': {e}")

try:
    # Chờ đến khi phần tử '30 ngày trước' hiển thị và nhấp
    button_30_days = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'30 ngày trước')]"))
    )
    button_30_days.click()
    print("Đã nhấp vào nút '30 ngày trước'.")
    sleep(2)
except Exception as e:
    print(f"Không thể nhấp vào nút '30 ngày trước': {e}")


try:
     # Danh sách các tọa độ x với y mặc định là 90 được lấy tự động từ Script di chuột trên đồ thị canvas đã thêm vào consle của trang web.
    x_coordinates = [
        40, 53, 67, 81, 94, 106, 121, 135, 
        149, 162, 175, 189, 203, 216, 229, 
        243, 256, 269, 283, 298, 311, 325, 
        338, 351, 367, 379, 392, 406, 420, 432
    ]
    # Lấy kích thước viewport
    viewport_size = browser.execute_script("return {width: window.innerWidth, height: window.innerHeight};")
    viewport_width = viewport_size["width"]
    viewport_height = viewport_size["height"]
    print(f"Kích thước viewport: {viewport_width}x{viewport_height}")
    
    # Tìm phần tử canvas
    canvas = browser.find_element(By.CSS_SELECTOR, "canvas[role='img']")
    print("Đã tìm thấy phần tử canvas.")
    
    # Lấy kích thước của canvas
    canvas_size = canvas.size
    canvas_width = canvas_size['width']
    canvas_height = canvas_size['height']
    
    # Kiểm tra xem canvas có nằm trong viewport không
    canvas_location = canvas.location
    canvas_x = canvas_location['x']
    canvas_y = canvas_location['y']
    
    if canvas_x + canvas_width > viewport_width or canvas_y + canvas_height > viewport_height:
        print("Canvas nằm ngoài viewport. Điều chỉnh viewport hoặc cuộn trang.")
        browser.execute_script("arguments[0].scrollIntoView();", canvas)

    # Tạo đối tượng ActionChains để thực hiện hành động chuột
    action_chains = ActionChains(browser)

    # Lặp qua các tọa độ x và thực hiện nhấp chuột với y = 90
    for x in x_coordinates:
        # Di chuyển tới tọa độ trên canvas và nhấp chuột
        action_chains.move_to_element_with_offset(canvas, x, 90).click().perform()
        sleep(0.5)  # Tạm dừng 0.5 giây giữa mỗi lần nhấp chuột
        try:
            tooltip_element = browser.find_element(By.CSS_SELECTOR, ".Component-LineChartHoverTip")
          
            browser.execute_script("arguments[0].scrollIntoView(true);", tooltip_element)

            date = tooltip_element.find_element(By.CSS_SELECTOR, ".text").text
            revenue = tooltip_element.find_element(By.CSS_SELECTOR, ".value").text
            print(f"Tọa độ ({x_step},{y_step}) - Ngày: {date} - Doanh thu: {revenue}")

            with open('doanhthu.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([date, revenue])  # Ghi dữ liệu ngày và doanh thu vào file CSV

        except Exception as e:
            print(f"Không lấy được thông tin doanh thu tại tọa độ : {x_step},{y_step}: {e}")

except Exception as e:
    print(f"Không thể tương tác với phần tử canvas hoặc lấy dữ liệu: {e}")
   

# Tìm các phần tử chứa thông tin
elements = browser.find_elements(By.CLASS_NAME, "item")

# Duyệt qua các phần tử để lấy dữ liệu
for element in elements:
    label = element.find_element(By.CLASS_NAME, "line-clamp-2").text
    value = element.find_element(By.CLASS_NAME, "value").text
    unit = element.find_element(By.CLASS_NAME, "unit").text
    print(f"{label}: {value} ({unit})")

#  đoạn này có thể dùng để lưu cookie để đỡ phải đăng nhâpj nhiều lần
# pickle.dump(browser.get_cookies(), open("my_cookie.pkl", "wb"))

# Đóng trình duyệt
browser.quit()
