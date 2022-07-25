
"""
base64
優點:可以將二進位制資料轉化為可列印字元，方便傳輸資料，對資料進行簡單的加密，肉眼安全。 
缺點：內容編碼後體積變大，編碼和解碼需要額外工作量
"""

import base64
import os

base64_message = ""

folder_path = os.path.dirname(os.path.abspath(__file__))
file_name = "2020-01-13T09-42-00.717_Master_Big.txt"
file_path = os.path.join(folder_path, file_name)
with open(file_path, 'rb') as binary_file:
    binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')

    print(base64_message)


file_path = os.path.join(folder_path, file_name+"1")

base64_img_bytes = base64_message.encode('utf-8')
with open(file_path, 'wb') as file_to_save:
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    file_to_save.write(decoded_image_data)
