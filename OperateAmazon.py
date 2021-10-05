from logging import exception
from TimeUtiltys import TimeUtiltys 
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from sys import exit

#Amazonの画面操作を行なうクラス
class OperateAmazon():
    #ログイン処理
    #driver : chromeのドライバー
    #login : ログインID
    #password : ログインパスワード
    #loginUrl : アマゾンのログイン画面のURL
    def Login(driver:webdriver.Chrome,login:str,password:str,loginUrl:str,headless:str):
        driver.get(loginUrl)
        try:
            certification = False
            driver.find_element_by_name("email").send_keys(login)
            driver.find_element_by_id("continue").click()
            driver.find_element_by_name("password").send_keys(password)
            driver.find_element_by_name("rememberMe").click()
            driver.find_element_by_id("signInSubmit").click()
            
            
                    
            if len(driver.find_elements_by_id("nav-link-accountList-nav-line-1")) > 0:
                span:WebElement = driver.find_element_by_id("nav-link-accountList-nav-line-1")
                print("アカウント名:" + span.text[:-2])
            else:
                if len(driver.find_elements_by_id("auth-error-message-box")) > 0:
                    raise Exception()
                else:
                    certification= True
                    raise Exception()
                           
            print(datetime.now())
            print("ログイン出来ました。")
        except Exception as e:
            print("ログインできませんでした。")
            if headless == "n":
                print("購入処理実行時刻前までに手動でやり直してください。")
            else:
                if certification :
                     while True:  
                        print("Amazonから認証メールが届いてますか？")
                        certificationMail= input("*y/n>")
                        if certificationMail == "y" or certificationMail == "n":
                            break
                        else:
                            print("yかnを入力してください")

                     if certificationMail == "y":
                        print("購入時刻までに認証処理を済ませておいてください。")
                     else:
                        while True:
                            finish = input("Enterキーを押して、最初からやり直してください。")
                            if not finish:
                                exit()
                else:
                    while True:
                        finish = input("Enterキーを押して、最初からやり直してください。")
                        if not finish:
                            exit()                      
            

    #購入処理
    #driver : chromeのドライバー
    #purchaseGoodsUrl : 購入商品のURL
    #checkColor : 指定されたカラー情報
    #checkSize : 指定されたサイズ情報
    #quantity : 指定された個数
    def Purchase(driver:webdriver.Chrome,purchaseGoodsUrl:str,checkColor:str,checkSize:str,quantity:str):
        
        TimeUtiltys.MakeSleep(0.88)

        driver.get(purchaseGoodsUrl)
        
        try:
            # カラー指定がある場合
            if checkColor != "":
                if len(driver.find_elements_by_id("color_name_" + checkColor)) > 0:
                    li:WebElement = driver.find_element_by_id("color_name_" + checkColor)
                    li.find_element_by_tag_name("button").click()
                else:
                    print("[error]カラーが存在しないか選択できませんでした。")
                    driver.quit()
                    return

            # サイズ指定がある場合
            if checkSize != "":
                if len(driver.find_elements_by_id("native_dropdown_selected_size_name")) > 0:
                    select = Select(driver.find_element_by_id("native_dropdown_selected_size_name"))
                    select.select_by_index(int(checkSize))  # optionタグを選択状態に
                elif len(driver.find_elements_by_id("size_name_" + checkSize)) > 0:
                    li:WebElement = driver.find_element_by_id("size_name_" + checkSize)
                    li.find_element_by_tag_name("button").click()
                else:
                    print("[error]サイズが存在しないか選択できませんでした。")
                    driver.quit()
                    return
                

            # 購入数指定がある場合
            if quantity != "":
                if len(driver.find_elements_by_id("quantity")) > 0:
                    select = Select(driver.find_element_by_id("quantity"))
                    select.select_by_value(quantity)  # optionタグを選択状態に
                else:
                    print("[error]個数選択ができませんでした。")
                    driver.quit()
                    return
                
            
            # 通常の注文か定期おとく便の選択が出てきたら通常の注文を選択する
            if len(driver.find_elements_by_id("newAccordionRow")) > 0:
                li:WebElement = driver.find_element_by_id("newAccordionRow")
                li.find_element_by_class_name("a-accordion-row-a11y").click()
                         
            if len(driver.find_elements_by_id("buy-now-button")) > 0:
                driver.find_element_by_id("buy-now-button").click()  # 失敗しそうな処理
            else:
                print("[error]「今すぐ買う」ボタンが存在しないか押せません。")
                driver.quit()
                return
        
            if len(driver.find_elements_by_name("placeYourOrder1")) > 0:
                # 画面遷移した場合
                driver.find_element_by_name("placeYourOrder1").click()  
                OperateAmazon.SuccessProsess(driver)
            else:
                # iframeになった場合
                try:                     
                    driver.switch_to_frame("turbo-checkout-iframe")
                    driver.find_element_by_xpath('//*[@id="turbo-checkout-pyo-button"]').click()
                    OperateAmazon.SuccessProsess(driver)
                except Exception as e:
                    print("[error]購入失敗")
                    driver.quit()
                    return                  
        
        except Exception as e:
            print("[error]存在しないページか対応していないページです。あるいは何らかの不具合が発生してます")
            driver.quit()

    #購入成功時の処理
    #driver : chromeのドライバー
    def SuccessProsess(driver:webdriver):
        print(datetime.now())
        print("[success]購入成功")
        sleep(5)
        driver.quit()
        

