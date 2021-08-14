import re

#バリデーション関係のクラス
class CheckUtiltys():
    #メールアドレスかどうか確認する
    #mail : メールアドレス
    #return : True(ok)/False(ng)
    def CheckMailAddress(mail:str):
        return re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", mail)
    
    #半角英数字記号かどうか確認する
    #target : 対象の文字列
    #return : True(ok)/False(ng)
    def CheckHankakuEisuziKigou(target:str):
        return re.match("^[a-zA-Z0-9!-/:-@¥[-`{-~]*$", target)

    #メールアドレスかどうか確認する
    #target : 対象の文字列
    #fqdn : 指定のFQDN
    #return : True(ok)/False(ng)  
    def CheckURL(target:str,fqdn:str):
        return re.match("https?://" + fqdn + "+", target)