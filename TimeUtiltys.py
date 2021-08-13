import NTPClient
import datetime
from time import perf_counter


class TimeUtiltys():

    #指定時間まで待機させる
    def MakeSleep(weitSec:float):
        until = perf_counter() + weitSec
        while perf_counter() < until:
            pass

    #Ntpサーバーの時間と指定時間の差を求める
    def FindTheTimeDifference(ts:datetime ,ntpClient:NTPClient):
        return ts.timestamp() - ntpClient.GetNowTime()

    
