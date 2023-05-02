import ntplib

#NTPクライアントで正しい時刻を取得させるクラス
class NTPClient(object):
    def __init__(self,ntp_server_host):
        self.ntp_client = ntplib.NTPClient()
        self.ntp_server_host = ntp_server_host
    #NTPクライアントから実時刻を求める
    #return : 実時刻
    def GetNowTime(self):      
        res = self.ntp_client.request(self.ntp_server_host) 
        return res.tx_time     