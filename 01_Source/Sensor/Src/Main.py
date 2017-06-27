# -*- coding: UTF-8 -*-

import os
import time
import math
import logging
import threading
import traceback
from datetime import datetime

import Setting
import Measurement
import Connection

class Main:
    """
    メインシーケンスを管理するクラス
    """
    
    def __init__(self):
        """
        コンストラクタ
        """
        
        try:
            logging.info("start.")
            
            # メンバ変数の初期化
            self.disposed = False
            
            self.measurement = None
            self.connection = None
            self.readAndPostDataThread = None
            self.finishEvent = None
            
            # Measurementインスタンス生成
            self.measurement = Measurement.Measurement()
            if self.measurement is None:
                raise Exception("Measurement create failed.")
            
            # Connectionインスタンス生成
            self.connection = Connection.Connection(Setting.USE_PROXY)
            if self.connection is None:
                raise Exception("Connection create failed.")
            
        except Exception as e:
            logging.error(str(e))
            raise
        except:
            logging.error(traceback.format_exc())
            raise
        finally:
            logging.info("finish.")
    
    def start_thread(self):
        """
        湿度の取得と送信を実施するスレッドの生成と起動
        """
        
        try:
            logging.info("start.")
            
            # スレッドの生成
            self.readAndPostDataThread = threading.Thread(target=self.read_and_post_data)
            if self.readAndPostDataThread is None:
                raise Exception("readAndPostDataThread create failed.")
            
            # スレッドの終了待ちイベントの生成
            self.finishEvent = threading.Event()
            if self.finishEvent is None:
                raise Exception("finishEvent create failed.")
            
            # スレッドの起動
            self.readAndPostDataThread.start()
        except:
            logging.error(traceback.format_exc())
            raise
        finally:
            logging.info("finish.")
    
    def read_and_post_data(self):
        """
        
        """
        
        logging.info("start.")
        
        try:
            while True:
                try:
                    # 現在時刻の取得
                    measurementTime = datetime.now()
                    
                    # 湿度の取得
                    pureData = self.measurement.read_data(Setting.ADC_PIN)
                    
                    # 湿度の正規化
                    normalizedData = self.normalize_data(pureData)
                    
                    # 湿度の送信
                    self.connection.post_data(Setting.SENSOR_ID, normalizedData, measurementTime)
                except KeyboardInterrupt:
                    logging.info("KeyboardInterrupt occured.")
                    # [Ctrl+C]を認識した場合は、ループから離脱する
                    break
                except:
                    logging.error(traceback.format_exc())
                finally:
                    # 指定時間だけ待機
                    time.sleep(Setting.PROCESS_INTERVAL);
        except KeyboardInterrupt:
            logging.info("KeyboardInterrupt occured.")
        except:
            logging.error(traceback.format_exc())
            raise
        finally:
            # スレッドの終了通知
            self.finishEvent.set()
            
            logging.info("finish.")
    
    def normalize_data(self, data):
        """
        データを正規化する
        
        @param data 正規化対象となるデータ
        @return 正規化したデータ
        """
        
        normalized = 0.0
        
        try:
            logging.info("start. data = " + str(data))
            
            # 指定した基準をもとに正規化
            baseValue = 2.0 ** Setting.RESOLUTION - 1.0
            normalized = data / baseValue * Setting.NORMALIZED_BASE
            
            # 有効桁数を考慮
            normalized = round(normalized, Setting.USE_DIGIT)
        except:
            logging.error(traceback.format_exc())
            raise
        finally:
            logging.info("finish. normalized = " + str(normalized))
        
        return normalized
    
    def dispose(self):
        """
        終了処理
        """
        
        try:
            logging.info("start.")
            
            # すでに終了処理が実行済みの場合はスキップする
            if self.disposed is False:
                # すでに予約済みのタイマーをキャンセル
                if self.readAndPostDataThread is not None:
                    self.readAndPostDataThread.cancel()
                    self.readAndPostDataThread = None
                
                # Measurementの終了処理
                if self.measurement is not None:
                    self.measurement = None
                
                # Connectionの終了処理
                if self.connection is not None:
                    self.connection = None
                
                self.disposed = True
        except:
            logging.error(traceback.format_exc())
            raise
        finally:
            logging.info("finish.")
    
    def __del__(self):
        """
        デストラクタ
        """
        
        try:
            logging.info("start.")
            
            self.dispose()
        except:
            logging.error(traceback.format_exc())
        finally:
            logging.info("finish.")
    

def main():
    """
    メイン関数
    """
    
    mainObj = None
    try:
        # ログフォルダ作成
        existLogFolder = os.path.exists(Setting.LOG_FILE_RELATIVE_PATH)
        if existLogFolder is False:
            os.mkdir(Setting.LOG_FILE_RELATIVE_PATH)
        
        # ログ出力基本情報設定
        currentDate = datetime.now().strftime("%Y%m%d")
        logFileName = currentDate + Setting.LOG_FILE_EXT
        logFilePath = os.path.join(Setting.LOG_FILE_RELATIVE_PATH, logFileName)
        logging.basicConfig(filename=logFilePath, level=Setting.LOG_FILE_LEVEL, format="%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d %(message)s")
        
        mainObj = Main()
        if mainObj is not None:
            # メインシーケンスの起動
            mainObj.start_thread()
            
            # メインシーケンスの終了待機
            mainObj.finishEvent.wait()
    except:
        logging.error(traceback.format_exc())
    finally:
        logging.info("finally start.")
        if mainObj is not None:
            # 終了処理
            mainObj.dispose()
        
        logging.info("finish.")

if __name__ == "__main__":
    main()
