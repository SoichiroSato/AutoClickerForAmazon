import TimeUtiltys 
import datetime
from selenium.webdriver.support.select import Select
import datetime
from selenium import webdriver

#正しい時刻を取得
class OperateAmazon():
   #ログイン処理
    def Login(driver : webdriver.Chrome,login :str,password :str,loginUrl :str):
        driver.get(loginUrl)
        try:
            driver.find_element_by_name("email").send_keys(login)
            driver.find_element_by_id("continue").click()
            driver.find_element_by_name("password").send_keys(password)
            driver.find_element_by_name("rememberMe").click()
            driver.find_element_by_id("signInSubmit").click()
            print(datetime.datetime.now())
            print("ログイン出来ました。念のため確認をお願いします。")
            print("ログイン出来ていない場合は手動でログインしてください。")
        except:
            print("ログインできませんでした。")
            print("購入処理実行時刻前までに手動でやり直してください。")
        finally:
            print("手動でログインする場合は「ログインしたままにする」にチェックをいれてください。")

    #購入処理
    def Purchase(driver : webdriver.Chrome,purchaseGoodsUrl :str,checkColor :str,checkSize :str,quantity:str):
        
        TimeUtiltys.TimeUtiltys .MakeSleep(0.88)

        driver.get(purchaseGoodsUrl)

        try:
            # カラー指定がある場合
            if checkColor != "":
                try:
                    index = int(checkColor) + 9
                    driver.find_element_by_id("a-autoid-" + str(index) + "-announce").click()
                except Exception as e:
                    print("[error]カラーが存在しないか選択できませんでした。")
                    return

            # サイズ指定がある場合
            if checkSize != "":
                try:
                    select = Select(driver.find_element_by_id('native_dropdown_selected_size_name'))
                    select.select_by_index(int(checkSize))  # optionタグを選択状態に
                except Exception as e:
                    print("[error]サイズが存在しないか選択できませんでした。")
                    return

            # 購入数指定がある場合
            if quantity != "":
                try:
                    select = Select(driver.find_element_by_id('quantity'))
                    select.select_by_value(quantity)  # optionタグを選択状態に
                except Exception as e:
                    print("[error]個数選択ができませんでした。")
                    return

            for _ in range(10):  # 最大10回実行。カラー、サイズ指定があるやつはすぐ表示されないことがあるため
                try:
                    driver.find_element_by_id('buy-now-button').click()  # 失敗しそうな処理
                except Exception as e:
                    pass  
                else:
                    break  # 失敗しなかった時はループを抜ける
            else:
                print("[error]「今すぐ買う」ボタンが存在しないか押せません。")
                return
            
            try:
                # 画面遷移した場合
                driver.find_element_by_name("placeYourOrder1").click()  
                print(datetime.datetime.now())
                print("[success]購入成功")
            except Exception as e:
                # iframeになった場合
                for _ in range(10):  # 最大10回実行
                    try:
                        driver.switch_to.frame("turbo-checkout-iframe")
                        driver.find_element_by_xpath('//*[@id="turbo-checkout-pyo-button"]').click()
                        print(datetime.datetime.now())
                        print("[success]購入成功")
                    except Exception as e:
                        pass  
                    else:
                        break  # 失敗しなかった時はループを抜ける
                else:
                    print("[error]購入失敗")
                    return
        
        except Exception as e:
            print("[error]Amazon以外のページか対応していないページです。あるいは何らかの不具合が発生してます")

