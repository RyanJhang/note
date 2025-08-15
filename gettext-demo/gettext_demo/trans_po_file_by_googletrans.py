import os
from googletrans import Translator
from polib import pofile, POEntry

# 設置翻譯器
translator = Translator()

# 定義要支援的語言
languages = ["en", "th", "vi", "zh-TW"]

# 獲取當前腳本所在目錄
base_dir = os.path.dirname(os.path.abspath(__file__))

# 根據py檔案，產生.pot
apppy = os.path.join(base_dir, "app.py")
pot_file_path = os.path.join(base_dir, "locales/base.pot")
os.system(
    f"xgettext -o {pot_file_path} {apppy}"
)

# 根據 .pot 產生 en_US的.po
po_file_path = os.path.join(base_dir, "locales/en/LC_MESSAGES/base.po")
os.makedirs(os.path.dirname(po_file_path), exist_ok=True)

os.system(
    f"msginit -l th_TH.UTF8 -o {po_file_path} -i {pot_file_path} --no-translator"
)

mo_file_path = os.path.join(base_dir, "locales/en/LC_MESSAGES/base.mo")
os.system(f"msgfmt -o {mo_file_path} {po_file_path}")

# 載入現有的 .po 檔範本
po_template = pofile(po_file_path)

# 翻譯成目標語系
for lang in languages:
    po_file_path = os.path.join(base_dir, f"locales/{lang}/LC_MESSAGES/base.po")
    os.makedirs(os.path.dirname(po_file_path), exist_ok=True)

    # 創建新的 .po 文件
    po = po_template.__class__()
    po.metadata = {"Content-Type": "text/plain; charset=UTF-8", "Language": lang}

    # 遍歷每個條目並翻譯
    for entry in po_template:
        print(entry.msgid)
        print(entry.msgstr)
        new_entry = POEntry(
            msgid=entry.msgid, msgstr=translator.translate(entry.msgid, dest=lang).text
        )
        po.append(new_entry)

    # 保存更新後的 .po 文件
    po.save(po_file_path)

    # 編譯 .po 文件為 .mo 文件
    mo_file_path = os.path.join(base_dir, f"locales/{lang}/LC_MESSAGES/base.mo")
    os.system(f"msgfmt -o {mo_file_path} {po_file_path}")
