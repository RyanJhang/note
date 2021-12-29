

import os
import json


from smb.SMBConnection import SMBConnection


folder_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(folder_path, "connection_info.json")

with open(json_path) as f:
    data = json.load(f)

connect_info = data["FACTORY_1"]

host = connect_info['ip']  # ip或域名
username = connect_info['username']
password = connect_info['password']
service_name = connect_info['service_name']
path = connect_info['dst_path']

conn = SMBConnection(username, password, "", "", use_ntlm_v2=True)
result = conn.connect(host, 445)
print("登錄成功")


files = conn.listPath(service_name, path)
file_names = []
for file in files:
    if file.filename not in [os.curdir, os.pardir]:
        file_names.append(file.filename)
print(file_names)
conn.close()
