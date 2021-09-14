from TimeUtiltys import TimeUtiltys 
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement
from time import sleep

#Amazonの画面操作を行なうクラス
class OperateAmazon():
    #ログイン処理
    #driver : chromeのドライバー
    #login : ログインID
    #password : ログインパスワード
    #loginUrl : アマゾンのログイン画面のURL
    def Login(driver:webdriver.Chrome,login:str,password:str,loginUrl:str):
        driver.get(loginUrl)
        try:
            driver.find_element_by_name("email").send_keys(login)
            driver.find_element_by_id("continue").click()
            driver.find_element_by_name("password").send_keys(password)
            driver.find_element_by_name("rememberMe").click()
            driver.find_element_by_id("signInSubmit").click()
            print(datetime.now())
            print("ログイン出来ました。念のため確認をお願いします。")
            print("ログイン出来ていない場合は手動でログインしてください。")
        except:
            print("ログインできませんでした。")
            print("購入処理実行時刻前までに手動でやり直してください。")
        finally:
            print("手動でログインする場合は「ログインしたままにする」にチェックをいれてください。")

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
                for _ in range(5):
                    try:
                        li:WebElement = driver.find_element_by_id("color_name_" + checkColor)
                        li.find_element_by_tag_name("button").click()
                    except Exception as e:
                        pass  
                    else:
                        break  # 失敗しなかった時はループを抜ける
                else:
                    print("[error]カラーが存在しないか選択できませんでした。")
                    driver.quit()
                    return

            # サイズ指定がある場合
            if checkSize != "":
                for _ in range(5):
                    try:
                        select = Select(driver.find_element_by_id("native_dropdown_selected_size_name"))
                        select.select_by_index(int(checkSize))  # optionタグを選択状態に
                        break
                    except Exception as e:
                        li:WebElement = driver.find_element_by_id("size_name_" + checkSize)
                        li.find_element_by_tag_name("button").click()
                        break
                    except Exception as e:
                        pass
                else:
                    print("[error]サイズが存在しないか選択できませんでした。")
                    driver.quit()
                    return

            # 購入数指定がある場合
            if quantity != "":
                for _ in range(5):
                    try:
                        select = Select(driver.find_element_by_id("quantity"))
                        select.select_by_value(quantity)  # optionタグを選択状態に
                    except Exception as e:
                        pass  
                    else:
                        break  # 失敗しなかった時はループを抜ける
                else:
                    print("[error]個数選択ができませんでした。")
                    driver.quit()
                    return
            
            # 通常の注文か定期おとく便の選択が出てきたら通常の注文を選択する
            try:
                li:WebElement = driver.find_element_by_id("newAccordionRow")
                li.find_element_by_class_name("a-accordion-row-a11y").click()
            except Exception as e:
                # なかったらスルー
                pass

            for _ in range(10):  # 最大10回実行。カラー、サイズ指定があるやつはすぐ表示されないことがあるため
                try:
                    driver.find_element_by_id("buy-now-button").click()  # 失敗しそうな処理
                except Exception as e:
                    pass  
                else:
                    break  # 失敗しなかった時はループを抜ける
            else:
                print("[error]「今すぐ買う」ボタンが存在しないか押せません。")
                driver.quit()
                return
            
            for _ in range(30):  # 最大30回実行
                try:
                    # 画面遷移した場合
                    driver.find_element_by_name("placeYourOrder1").click()  
                    print(datetime.now())
                    print("[success]購入成功")
                    sleep(5)
                    driver.quit()
                    break
                except Exception as e:
                    # iframeになった場合                     
                    driver.switch_to_frame("turbo-checkout-iframe")
                    driver.find_element_by_xpath('//*[@id="turbo-checkout-pyo-button"]').click()
                    print(datetime.now())
                    print("[success]購入成功")
                    sleep(5)
                    driver.quit()
                    break
                except Exception as e:
                    pass           
            else:
                print("[error]購入失敗")
                driver.quit()
                return
        
        except Exception as e:
            print("[error]存在しないページか対応していないページです。あるいは何らかの不具合が発生してます")
            driver.quit()

