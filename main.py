import OperateAmazon 
import NTPClient
import Config
import TimeUtiltys 
import CheckUtiltys
import datetime
from time import sleep
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

#Amazonの自動購入プログラム
def main():
    
    print("・このプログラムは「今すぐ買う」ボタンがあるページのみ使えます。")
    print("・このプログラムはオプション指定なしの商品、衣類のみ使えます。")
    print("・カートの中身は空にしておいてください。")
    print("・このプログラムでの購入決済方法は「クレジットカード」を推奨します。")
    print("・各入力項目は入力後に「Enter」キーを押してください。")
    print("・[*]がある入力項目は必須です。ないものは任意で設定してください。")

    LOGIN_URL = "https://www.amazon.co.jp/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=jpflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
    while True:   
        login = input("*ログインID(半角)>")
        if login != "":
            if CheckUtiltys.CheckUtiltys.CheckMailAddress(login):
                break
            else:
                print("ログインIDが不正です。")
        else:
            print("ログインID(半角)は必須です。")
    while True:  
        password = input("*ログインPassWord(半角)>")
        if password != "":
            if CheckUtiltys.CheckUtiltys.CheckHankakuEisuziKigou(password):
                break
            else:
                print("passwordが不正です。")
        else:
            print("ログインPassWord(半角)は必須です。")
    while True:
        purchaseGoodsUrl = input("*買いたい商品のURL>")
        if purchaseGoodsUrl != "":
            if CheckUtiltys.CheckUtiltys.CheckURL(purchaseGoodsUrl,"www.amazon.co.jp"):
                break
            else:
                print("AmazonのURLを入力してください。")
        else:
            print("買いたい商品のURLは必須です。")

    checkColor = input("カラーを選択する場合は左または上から順に0から半角数値で入力してください。未入力可。(例)一番左を選択の場合「0」>")
    checkSize = input("サイズを選択する場合は左または上から順に0から半角数値で入力してください。未入力可。(例)一番上を選択の場合「0」>")
    quantity = input("2つ以上購入する場合は購入個数を入力してください。1つの場合は未入力でエンターキーを押してください。>")

    while True:
        try:
            start = datetime.datetime.strptime(input("*開始時間(hh:mm) ※現在時刻より最低3分後>") + ":00","%H:%M:%S").time()
            before2Minites = datetime.datetime.combine(datetime.date.today(), start) - datetime.timedelta(minutes=2)
            loginTime = datetime.datetime.combine(datetime.date.today(), before2Minites.time()) #購入予定時刻の2分前
            before1Seconds = datetime.datetime.combine(datetime.date.today(), start) - datetime.timedelta(seconds=1)
            purchaseTime = datetime.datetime.combine(datetime.date.today(), before1Seconds.time()) #購入予定時刻の1秒前
            break
        except Exception as e:
            print("[error]開始時刻が不正です。もう一度入力してください")
            continue

    print("ログイン処理実行時刻:"+str(loginTime))
    print("購入処理実行時刻:"+str(purchaseTime))

    ntpClient = NTPClient.NTPClient("ntp.nict.jp")
    
    TimeUtiltys.TimeUtiltys.MakeSleep(TimeUtiltys.TimeUtiltys.FindTheTimeDifference(loginTime,ntpClient))

    options = webdriver.ChromeOptions()
    options.add_argument('--incognito') 
    driver = webdriver.Chrome(Config.Config.resource_path("./chromedriver/chromedriver.exe"),chrome_options=options)
    wait = WebDriverWait(driver, 30) #指定したdriverに対して最大で10秒間待つように設定する

    OperateAmazon.OperateAmazon.Login(driver,login,password,LOGIN_URL)
    
    TimeUtiltys.TimeUtiltys.MakeSleep(TimeUtiltys.TimeUtiltys.FindTheTimeDifference(purchaseTime,ntpClient))

    OperateAmazon.OperateAmazon.Purchase(driver,purchaseGoodsUrl,checkColor,checkSize,quantity)

    sleep(5)
    driver.quit()

    while True:
        finish = input("終了するにはEnterキーを押してください")
        if not finish:
            break
    
main()
