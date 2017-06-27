# -*- coding: UTF-8 -*-

import logging
import traceback
import time
import os
import RPi.GPIO as GPIO

import Setting

class Measurement:
    """
    土壌センサーから湿度を計測するクラス
    """
    
    def __init__(self):
        """
        コンストラクタ
        """
        
        try:
            logging.info("start.")
            
            # SPIピンをBCM番号で指定
            GPIO.setmode(GPIO.BCM)
            
            # SPIピンのSetup
            GPIO.setup(Setting.SPI_MOSI, GPIO.OUT)
            GPIO.setup(Setting.SPI_MISO, GPIO.IN)
            GPIO.setup(Setting.SPI_CLK, GPIO.OUT)
            GPIO.setup(Setting.SPI_CS, GPIO.OUT)
        except:
            logging.error(traceback.format_exc())
            raise
        finally:
            logging.info("finish.")
    
    def read_data(self, adcpin):
        """
        データの読み取り処理
        
        @param adcpin ADコンバーターで使用するピン番号（チャネル番号）
        @return 土壌センサーから読み込みAD変換したデータ
        """
        
        adcout = 0
        
        try:
            logging.info("start.")
            
            clockpin = Setting.SPI_CLK
            mosipin = Setting.SPI_MOSI
            misopin = Setting.SPI_MISO
            cspin = Setting.SPI_CS
            commandout = adcpin
            
            if ((commandout > Setting.ADC_PIN_MAX) or (commandout < Setting.ADC_PIN_MIN)):
                return -1
            commandout |= 0x18  # start bit + single-ended bit
            commandout <<= 3  # we only need to send 5 bits here
            
            # 念のためTrueにしておく
            GPIO.output(cspin, True)
            
            # 読み取り処理開始
            GPIO.output(clockpin, False)
            GPIO.output(cspin, False)
            
            # D_INのビット読み取り
            for i in range(Setting.ADC_START_BIT):
                if (commandout & 0x80):
                    GPIO.output(mosipin, True)
                else:
                    GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
            
            # D_OUTのビット読み取り（NullBit含む）
            for i in range(Setting.RESOLUTION + 1):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                    adcout |= 0x1
            
            # 読み取り処理完了
            GPIO.output(cspin, True)
            
            # [DEBUG]最終的にはprint文は削除する
            print("{0}".format(adcout) + " : " + "{0}%".format(round(adcout / 40.95, 1)))
            return adcout
        except:
            logging.error(traceback.format_exc())
            raise
        finally:
            logging.debug("finish.")
    
