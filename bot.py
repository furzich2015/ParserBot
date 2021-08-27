import os
import random
import names
import pickle
import sqlite3
from sqlite3 import Error
import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

while True:
    def BotPars():
        connection = sqlite3.connect('database.sqlite')
        cursor = connection.cursor()
        cursor.execute(" CREATE TABLE IF NOT EXISTS random (randomname text)")
        connection.commit()
        cursor.execute(" SELECT randomname FROM random WHERE randomname = randomname ")
        randomName = cursor.fetchone()
        if randomName is None:
            createName = names.get_first_name()
            cursor.execute(" INSERT INTO random (randomname) VALUES (?)", (createName,))
            connection.commit()
        elif randomName is True:
            print('КОРИСТУВАЧ СТВОРЕНО')

        cursor.execute(""" SELECT randomname FROM random """)
        while True:
            row = cursor.fetchone()
            if row == None:
                break
            randomNameCreated = (row[0])
        cursor.close()
        connection.close()

        #Получаем абсолютний путь
        absolutePatch = os.path.abspath('./')

        #ПРОВЕРЯЕМ ДЕРИКТОРИЮ НА СУЩЕСВОВАНИЕ
        check_directory = os.path.exists(f"{absolutePatch}\\Users\\{randomNameCreated}\\AppData\\Local\\Google\\Chrome\\Userdata")
        if check_directory is True:
            print('ПАПКА З КОРИСТУВАЧОМ - ЗНАЙДЕНО')
        elif check_directory is False:
            os.makedirs(f"{absolutePatch}\\Users\\{randomNameCreated}\\AppData\\Local\\Google\\Chrome\\Userdata")
            print('ПАПКИ З КОРИСТУВАЧОМ - НЕ ЗНАЙДЕНО, СТВОРЮЮ')

        #ПАРЕМЕТРИ GOOGLE CHROME
        options = Options()
        options.add_argument("--disable-blink-features")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument("--disable-dev-shm-using")
        options.add_argument("--disable-extensions")
#       options.add_argument("--disable-gpu")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--window-size=800,800")
        options.add_argument("log-level=3")
        #options.add_argument("--headless")
        options.add_argument(f"user-data-dir={absolutePatch}\\Users\\{randomNameCreated}\\AppData\\Local\\Google\\Chrome\\Userdata")
        options.add_argument("--profile-directory=Profile1")
        driver = webdriver.Chrome(executable_path=r'driver\chromedriver.exe', chrome_options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            const newProto = navigator.__proto__
            delete newProto.webdriver
            navigator.__proto__ = newProto
            """
        })
        driver.get('https://www.aplus-automotive.com.ua/products?')
        checkSession = os.path.isfile('session')
        if checkSession is True:
            for cookie in pickle.load(open('session', 'rb')):
                driver.add_cookie(cookie)
        sleep(5)
        #takeLinks = driver.find_element_by_xpath('//*[@id="spares-table"]/tbody/tr[2]/td[1]/div/a').get_attribute("href")
        reklama = driver.find_element_by_xpath('//*[@id="lightbox"]/div[2]/div/div[2]/a')
        if reklama.is_displayed() is True:
            reklama.click()
            print('Реклама закрита')
        i = 1
        while i <= 0:
            print(i)
            pages = driver.find_elements_by_id(f'page-{i}')
            for page in pages:
                print(page)
                page.click()
                sleep(10)
                #takeLinks = WebDriverWait(driver,30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"product_details_link")))
                takeLinks = driver.find_elements_by_class_name('product_details_link')
                with open("tovar.txt", "a") as txt_file:
                    for n in takeLinks:
                        takeLinks = n.get_attribute('href')
                        txt_file.write(takeLinks)
                        txt_file.write("\n")
                        txt_file.close
                        #print(takeLinks)
                        takeLinks = set()
                with open("tovar.txt", "r") as fp:
                    for line in fp.readlines():
                        takeLinks.add(line)
                with open("GoodUrl.txt", "a") as fp:
                    for line in takeLinks:
                        fp.write(line)
                        print(line)
            i = i + 1
        try:
            with connect(
                host="37.46.255.251:3306",
                user="root",
                password="",
            ) as connection:
                print(connection)
        except Error as e:
            print(e)
        #cursor = connection.cursor()
        goodUrlReady = open("GoodUrl.txt", "r")
        readyGoodUrl = goodUrlReady.readlines()
        for link in readyGoodUrl:
            driver.get(link)
            sleep(5)
            parnaDetailsVisible = driver.find_element_by_xpath('//*[@id="urun-bilgileri"]/div[3]').is_displayed()
            print(parnaDetailsVisible)
            if parnaDetailsVisible is True:
                parnaDetails = driver.find_elements_by_xpath('//*[@id="urun-bilgileri"]/div[3]/span/a')
                for parnaDetailsGetText in parnaDetails:
                    print(parnaDetailsGetText.text)
                    continue
            elif parnaDetailsVisible is False:
                applusNumber = driver.find_element_by_class_name('urun-kodu').text
                print(f"Номер APLUS - {applusNumber}")
                nameTovara = driver.find_element_by_class_name('urun-basligi').text
                print(f"Назва товару - {nameTovara}")
                productsMarka = driver.find_elements_by_xpath('//*[@id="urun-detaylari-sol-kisim"]/table/tbody/tr/td[1]')
                for productMarka in productsMarka:
                    print(productMarka.text)
                productsModel = driver.find_elements_by_xpath('//*[@id="urun-detaylari-sol-kisim"]/table/tbody/tr/td/div[1]')
                for productModel in productsModel:
                    print(productModel.text)
                productsModeldiv2 = driver.find_elements_by_xpath('//*[@id="urun-detaylari-sol-kisim"]/table/tbody/tr/td/div[2]')
                for productModeldiv2 in productsModeldiv2:
                    print(productModeldiv2.text)
                productsAgeModel = driver.find_elements_by_xpath('//*[@id="urun-detaylari-sol-kisim"]/table/tbody/tr/td[3]')
                for productAgeModel in productsAgeModel:
                    print(productAgeModel.text)
                print("-----------------------------------------")
                print("-----------Властивості деталі------------")
                print("-----------------------------------------")
                productsDetails = driver.find_elements_by_xpath('//*[@id="urun-ozellikleri-sag-kisim"]/table/tbody/tr/td')
                for productDetails in productsDetails:
                    print(productDetails.text)
                print("-----------------------------------------")
                print("-----------OEM Номера товару-------------")
                print("-----------------------------------------")
                productsOEM = driver.find_elements_by_xpath('//*[@id="urun-oem-numaralari"]/div/div[2]')
                for productOEM in productsOEM:
                    print(productOEM.text)
                sleep(1)
    BotPars()
    sleep(1000)