from NTPClient import NTPClient
from datetime import datetime 
from time import perf_counter

#時間操作処理のクラス
class TimeUtility():

    #指定時間まで待機させる
    #WaitSec : 指定時間
    def Sleep(waitSec:float):
        until = perf_counter() + waitSec
        while perf_counter() < until:
            pass
    #Ntpサーバーの時間と指定時間の差を求める
    #ts : パソコンの時刻
    #NTPClient : NTPクライアントオブジェクト
    #return : 時刻のずれ
    def FindTheTimeDifference(ts:datetime ,ntpClient:NTPClient):
        return ts.timestamp() - ntpClient.GetNowTime()
