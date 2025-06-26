from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# オプション設定（ヘッドレスモード）
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# ChromeDriverの場所を指定（同じフォルダ内にある場合）
service = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# 対象のURL
url = "https://www.tokyomotion.net/video/4554817/123456"
driver.get(url)

# 少し待機（JavaScriptの読み込み待ち）
time.sleep(3)

# iframe（埋め込み）の取得
iframe = driver.find_element("tag name", "iframe")
print("✅ 埋め込みURL:", iframe.get_attribute("src"))

driver.quit()
