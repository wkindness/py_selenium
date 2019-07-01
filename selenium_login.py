# python3.6
# selenium
# pandas
##################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

# chromedriverの設定
options = Options()
options.add_argument('--headless') # ヘッドレス設定
driver = webdriver.Chrome('./chromedriver_win32/chromedriver', chrome_options=options)
#driver = webdriver.Chrome('./chromedriver_win32/chromedriver')

url = 'https://server/login/'

#ファイル読み込み
df = pd.read_csv('user.csv') #userid, password（ヘッダ行あり）
count = len(df)
#出力ファイル
f = open('cookies.txt','w')

for i in range(count):
    userid = df.values[i, 0]
    password = df.values[i, 1]
    #ログイン
    driver.get(url)
    driver.find_element_by_id('userid').send_keys(userid)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('password').submit()
    time.sleep(2)

    # Cookies取得
    cookies = driver.get_cookies()
    for c in cookies:
        # 特定のCookiesを抽出
        if c["name"] == "auth_token":
            #「userid,auth_token」カンマ区切りで出力
            f.write(str(userid) + ',' + c["value"] + '\n')
            break

    # Cookies削除
    driver.delete_all_cookies()

f.close()
driver.quit()
