from NTPClient import NTPClient
from datetime import datetime 
from time import perf_counter

#時間操作処理のクラス
class TimeUtiltys():

    #指定時間まで待機させる
    #weitSec : 指定時間
    def MakeSleep(weitSec:float):
        until = perf_counter() + weitSec
        while perf_counter() < until:
            pass

    #Ntpサーバーの時間と指定時間の差を求める
    #ts : パソコンの時刻
    #NTPClient : NTPクライアントオブジェクト
    #return : 時刻のずれ
    def FindTheTimeDifference(ts:datetime ,ntpClient:NTPClient):
        return ts.timestamp() - ntpClient.GetNowTime()

    
