# -*- coding: UTF-8 -*-

import time
import json
import logging
import requests
import traceback
from datetime import datetime

import Setting

class Connection:
    """
    Webクラウドとの通信をするクラス
    
    Webクラウドとの通信が切断されていても、処理を継続する必要があるため、
    本クラスのAPIは、コンストラクタを除いて例外を補足しても、さらなる例外を発生させない。
    """
    
    def __init__(self, useProxy):
        """
        コンストラクタ
        
        @param useProxy プロキシを使用するかどうかのフラグ
        """
        
        try:
            logging.info("start.")
            
            # プロキシ設定
            self.proxies = None
            if useProxy is True:
                self.proxies = {
                    "http": Setting.PROXY,
                }
            
            # ヘッダ情報設定
            self.headers = {
                "Content-Type": "application/json"
            }
        except:
            logging.error(traceback.format_exc())
            raise
        finally:
            logging.info("finish.")
    
    def post_data(self, sensorId, humidity, measurementTime):
        """
        指定したデータリストをクラウドDBに送信(POST)する関数
        
        @param1 sensorId 土壌センサーの識別ID
        @param2 humidity 土壌センサーから取得した湿度
        @param3 measurementTime 土壌センサーから取得した測定時刻
        
        @remark 送信するデータ形式は下記の通り
                    value = {
                        "sensor_id": 1,
                        "humidity": 77.2,
                        "mesurement_time": "2017-06-08T19:39:20.617Z"
                    }
        """
        
        response = None
        latestTime = ""
        
        try:
            logging.info("start. sensorId = " + str(sensorId) + ", humidity = " + str(humidity) + ", measurementTime = " + str(measurementTime))
            
            # 時刻をフォーマット通りに成型
            formatedTime = measurementTime.strftime(Setting.DATETIME_DB_FORMAT)
            formatedTime = formatedTime[0:-3] + Setting.DATETIME_DB_FORMAT_Z
            
            # POST送信するJSON形式のデータを作成
            postData = {
                Setting.KEY_SENSOR_ID: sensorId,
                Setting.KEY_HUMIDITY: humidity,
                Setting.KEY_MEASUREMENT_TIME: formatedTime
            }
            logging.info("postData = " + str(postData))
            
            for i in range(Setting.REQUEST_RETRY_TIMES):
                # POST実行
                response = requests.post(Setting.URL, proxies=self.proxies, data=json.dumps(postData), headers=self.headers, timeout=Setting.REQUEST_TIMEOUT)
                logging.info("requests.post done.")
                
                # レスポンスの確認
                if response.status_code == Setting.STATUS_CODE_SUCCESS:
                    # レスポンスをJSON形式で取得
                    retData = response.json()
                    logging.debug("retData = " + str(retData))
                    
                    # 送信成功でループ脱出
                    break
                else:
                    logging.error("requests.post failed. status_code = " + str(response.status_code))
                    
                    # 送信失敗でリトライ間隔だけ待機
                    time.sleep(Setting.REQUEST_RETRY_INTERVAL)
        except:
            logging.error(traceback.format_exc())
            if response is not None:
                logging.error("response = " + str(response))
            raise
        finally:
            logging.info("finish.")
    
