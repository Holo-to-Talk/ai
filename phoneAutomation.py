from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from constants import PhoneAutomationSettings
import os
import time

# 電話をかける
def phoneAutomation():
    # URL取得
    URL = PhoneAutomationSettings.URL

    # 代表電話番号取得
    PHONE_NUMBER = PhoneAutomationSettings.PHONE_NUMBER

    # Driver Wait Time秒数取得
    WEB_DRIVER_WAIT_TIME = PhoneAutomationSettings.WEB_DRIVER_WAIT_TIME

    # Time Sleep秒数取得
    TIME_SLEEP_TIME = PhoneAutomationSettings.TIME_SLEEP_TIME

    # オプション
    options = Options()
    options.add_argument('--use-fake-ui-for-media-stream')
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')

    # Chrome起動
    driver = webdriver.Chrome(options = options)

    # URL遷移
    driver.get(URL)

    startUpButton = WebDriverWait(driver, WEB_DRIVER_WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="startup-button"]'))
    )
    startUpButton.click()

    getDevicesButton = WebDriverWait(driver, WEB_DRIVER_WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="get-devices"]'))
    )
    getDevicesButton.click()

    phoneNumberInput = WebDriverWait(driver, WEB_DRIVER_WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="phone-number"]'))
    )
    phoneNumberInput.send_keys(PHONE_NUMBER)

    callButton = WebDriverWait(driver, WEB_DRIVER_WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="button-call"]'))
    )
    callButton.click()

    hangUpOutGoingButton = WebDriverWait(driver, WEB_DRIVER_WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="button-hangup-outgoing"]'))
    )

    while True:
        # クラス取得
        hangUpOutGoingButton_className = hangUpOutGoingButton.get_attribute('class')
        # hideというクラスがあるかどうか
        if 'hide' in hangUpOutGoingButton_className.split():
            # 終了
            driver.quit()

            break

        else:
            # 待機
            time.sleep(TIME_SLEEP_TIME)