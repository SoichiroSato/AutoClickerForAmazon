

import datetime
from time import ctime, perf_counter, sleep
import ntplib
from selenium.webdriver.support.select import Select
from time import sleep
import datetime
from datetime import timedelta
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("このプログラムは今すぐ買うボタンがあるページのみ使えます")
print("このプログラムはオプション指定なしの商品、衣類のみ使えます")
print("カートの中身は空にしておいてください。")

url1 = "https://www.amazon.co.jp/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=jpflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
url2 = input("買いたい商品のURL>")
checkColor = input("カラーを選択する場合は左または上から順に0から番号を入力してください。ない場合は未入力でエンターキーを押してください。(例)一番左を選択の場合「0」>")
checkSize = input("サイズを選択する場合は左または上から順に0から番号を入力してください。ない場合は未入力でエンターキーを押してください。(例)一番上を選択の場合「0」>")
quantity = input("2つ以上購入する場合は購入個数を入力してください。1つの場合は未入力でエンターキーを押してください。>")
login = input("ID>")
password = input("Pass>")
start = input("開始時間(hh:mm:ss) ※現在時刻より最低3分後>")

start1 = datetime.datetime.strptime(start,'%H:%M:%S').time()
start2 = datetime.datetime.combine(datetime.date.today(), start1) - datetime.timedelta(minutes=2)
time_login = datetime.datetime.combine(datetime.date.today(), start2.time()) #購入予定時刻の2分前
start3 = datetime.datetime.combine(datetime.date.today(), start1) - datetime.timedelta(seconds=1)
time_main = datetime.datetime.combine(datetime.date.today(), start3.time()) #購入予定時刻の1秒前

print("ログイン処理実行時刻:"+str(time_login))
print("購入処理実行時刻:"+str(time_main))

#正しい時刻を取得
class NTPClient(object):
   def __init__(self, ntp_server_host):
       self.ntp_client = ntplib.NTPClient()
       self.ntp_server_host = ntp_server_host

   def GetNowTime(self, timeformat = '%Y/%m/%d %H:%M:%S'):      
       res = self.ntp_client.request(self.ntp_server_host) 
       return res.tx_time
       
ntpClient = NTPClient('ntp.nict.jp')

class MyError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "今すぐ買うボタンが存在しないか押せません。"

#待機時間を設定
def MakeSleep(ts):
   return ts.timestamp() - ntpClient.GetNowTime()

class cssSelectorError():
    def __init__(self):
        pass

    def __str__(self):
        return "Hi I'm MyError!"
#ログイン処理
def Login():
    driver.get(url1)
    try:
        driver.find_element_by_name("email").send_keys(login)
        driver.find_element_by_id("continue").click()
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_name("rememberMe").click()
        driver.find_element_by_id("signInSubmit").click()
    except:
        print("ログインできませんでした。手動でやり直してください。")
    print(datetime.datetime.now())
    print("ログイン出来ました。念のため確認をお願いします。")
    print("ログイン出来ていない場合は手動でログインしてください。")

#購入処理
def Buy():
    wait_sec = 0.88
    until = perf_counter() + wait_sec
    while perf_counter() < until:
        pass
    driver.get(url2)
    try:
        # カラー指定がある場合
        if checkColor != "":
            index = int(checkColor) + 9
            driver.find_element_by_id("a-autoid-" + str(index) + "-announce").click()

        # サイズ指定がある場合
        if checkSize != "":
            select = Select(driver.find_element_by_id('native_dropdown_selected_size_name'))
            select.select_by_index(int(checkSize))  # optionタグを選択状態に

        # 購入数指定がある場合
        if quantity != "":
            select = Select(driver.find_element_by_id('quantity'))
            select.select_by_value(quantity)  # optionタグを選択状態に

        for _ in range(3):  # 最大10回実行。カラー、サイズ指定があるやつはすぐ表示されないことがあるため
            try:
                driver.find_element_by_id('buy-now-button').click()  # 失敗しそうな処理
            except Exception as e:
                pass  # 必要であれば失敗時の処理
            else:
                break  # 失敗しなかった時はループを抜ける
        else:
            raise MyError()   
        
        try:
            # 画面遷移した場合
            driver.find_element_by_name("placeYourOrder1").click()  # 失敗しそうな処理
            print(datetime.datetime.now())
            print("購入成功")
        except Exception as e:
            # iframeになった場合
            for _ in range(10):  # 最大3回実行
                try:
                    driver.switch_to.frame("turbo-checkout-iframe")
                    driver.find_element_by_xpath('//*[@id="turbo-checkout-pyo-button"]').click()
                    print(datetime.datetime.now())
                    print("購入成功")
                except Exception as e:
                    pass  # 必要であれば失敗時の処理
                else:
                    break  # 失敗しなかった時はループを抜ける
            else:
                raise Exception("")   
        except Exception as e:
            print("購入失敗")
    except MyError as e:
        print(e)
    except Exception as e:
        print("Amazon以外のページか対応していないページです。あるいは何らかの不具合が発生してます")
    finally:
        sleep(5)
        driver.quit()
        
    
#メイン処理
wait_sec = MakeSleep(time_login)
until = perf_counter() + wait_sec
while perf_counter() < until:
   pass

options = webdriver.ChromeOptions()
options.add_argument('--incognito') 
driver = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(driver, 30) #指定したdriverに対して最大で10秒間待つように設定する

Login()
wait_sec = MakeSleep(time_main)
until = perf_counter() + wait_sec
while perf_counter() < until:
   pass

Buy()

