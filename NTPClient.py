import ntplib

#正しい時刻を取得
class NTPClient(object):
   def __init__(self, ntp_server_host ):
       self.ntp_client = ntplib.NTPClient()
       self.ntp_server_host = ntp_server_host

   def GetNowTime(self, timeformat = "%Y/%m/%d %H:%M:%S"):      
       res = self.ntp_client.request(self.ntp_server_host) 
       return res.tx_time     