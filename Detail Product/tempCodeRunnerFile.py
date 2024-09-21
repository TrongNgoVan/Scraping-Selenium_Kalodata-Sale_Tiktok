import pandas as pd

# Đọc tệp CSV
df = pd.read_csv('B:\Documents\PreprocessingData-main\PreprocessingData-main\PreprocessingData.csv')

# Kiểm tra tổng số dữ liệu thiếu trong mỗi cột
missing_data = df.isnull().sum()

print(missing_data)
