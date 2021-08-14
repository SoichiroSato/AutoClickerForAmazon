import sys
import os

#設定関係のクラス
class Config():
    #exe化したときに正しくパスを通させる
    #relative_path : Path
    #return : 正しいパス
    def resource_path(relative_path:str):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)

