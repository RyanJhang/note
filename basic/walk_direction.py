import os

folder_path = os.path.dirname(os.path.abspath(__file__))
folder_path = r"C:\Users\ryan.jhang\Downloads"

for dirPath, dirNames, fileNames in os.walk(folder_path):
    # print(dirPath)
    for f in fileNames:
        if ".qrc" in f:
            print(f'<include location="{os.path.join(dirPath, f)}"/>')
