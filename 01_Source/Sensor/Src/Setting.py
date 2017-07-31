# -*- coding: UTF-8 -*-

import logging

##### センサーごとに一意のIDに変更すること #####
# センサー識別ID
SENSOR_ID = 1
################################################



##### Main.py #####
# ログ出力のパラメータ
LOG_FILE_RELATIVE_PATH = "../Log"
LOG_FILE_EXT = ".log"
LOG_FILE_LEVEL = logging.INFO

# ログファイル保存期間（日）
LOG_STORAGE_DAYS = 10

# 正規化のための基準
NORMALIZED_BASE = 100

# 有効桁数（小数点第X位）
USE_DIGIT = 1

# メインシーケンスの実行間隔(秒)
PROCESS_INTERVAL = 3600
#PROCESS_INTERVAL = 1



##### Measurement.py #####
# ADコンバーターの分解能(D_OUTビット数)
# ※実際にはこの数にNullBitの1ビットを加えた数になる
RESOLUTION = 12

# ADコンバーターのD_INビット数
ADC_START_BIT = 5

# ADコンバーターの使用ピン(0～7指定)
ADC_PIN = 0
ADC_PIN_MIN = 0
ADC_PIN_MAX = 7

# ADコンバーターと関連付いたSPIピン番号
SPI_CLK = 11
SPI_MISO = 9
SPI_MOSI = 10
SPI_CS = 8


##### Connection.py #####
# WebAPI用パラメータ
URL = "http://172.24.215.178:9000/v2/humidity"
#URL = "http://172.24.215.229:9400/humidity"

# プロキシ設定
USE_PROXY = True
PROXY = "http://proxy.toyoko-sys.co.jp:8080"

# JSONフォーマット
KEY_SENSOR_ID = "sensor_id"
KEY_HUMIDITY = "humidity"
KEY_MEASUREMENT_TIME = "measurement_time"
KEY_CODE = "code"

DATETIME_DB_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"   # "Z"はマイクロ秒削除後につける
DATETIME_DB_FORMAT_Z = "Z"

# WebAPIリクエストのタイムアウト時間(秒)
REQUEST_TIMEOUT = 10

# WebAPIリクエストのリトライ間隔(秒)と回数
REQUEST_RETRY_INTERVAL = 1
REQUEST_RETRY_TIMES = 3

# レスポンスのステータスコード
STATUS_CODE_SUCCESS = 200
STATUS_CODE_INVALID = 405


