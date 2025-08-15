import gettext
import os

def set_language(lang):
    locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
    lang_trans = gettext.translation('base', localedir=locales_dir, languages=[lang])
    lang_trans.install()
    return lang_trans.gettext

# 初始設置為繁體中文
_ = set_language('zh-TW')
print(_("Hello, World!"))  # 應顯示 "你好，世界！"
print(_("hi barcode"))  # 應顯示 "你好，世界！"

# 切換到泰文
# 該語系檔案被砍掉，如何選到default?
_ = set_language('th')
print(_("Hello, World!"))  # 應顯示 "สวัสดีชาวโลก!"