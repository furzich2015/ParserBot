import os
import random
from sqlite3.dbapi2 import DateFromTicks
from typing import IO
import names
import pickle
import sqlite3
import urllib
import urllib.request
import requests
from colorama import init
from termcolor import RESET, colored
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
from selenium.common.exceptions import NoAlertPresentException, StaleElementReferenceException, TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

while True:
    def BotPars():
        print(colored('-' * 50, 'red'))
        print(colored('|---> Project: BotsPars APPlus v1.0', 'green'))
        print(colored('|--> Author: Vadym Pakhalchuk', 'green'))
        print(colored('|-> GIthub: https://github.com/furzich2015', 'green'))
        print(colored('-' * 50, 'red'))
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
        if check_directory is False:
            os.makedirs(f"{absolutePatch}\\Users\\{randomNameCreated}\\AppData\\Local\\Google\\Chrome\\Userdata")

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
        options.add_argument("maximize_window")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
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
                #Перевірка на наявність реклами
        sleep(2)     
        reklama = driver.find_element_by_xpath('//*[@id="lightbox"]/div[2]/div/div[2]/a')
        if reklama.is_displayed() is True:
            reklama.click()
            print('Реклама закрита')
        sleep(2)
        try:
            FindButtonAuth = driver.find_element_by_xpath('//*[@id="header-content"]/div[3]/div[4]/div/span')
            if FindButtonAuth.is_displayed() is True:
                print(colored('В аккаунт не авторизовано! Авторизуюсь', 'red'))
                ClickButtomLogin = driver.find_element_by_xpath('//*[@id="header-content"]/div[3]/div[4]/div/button')
                ClickButtomLogin.click()
                sleep(5)
                login = 'tir-rivne-auto@ukr.net'
                password = '2236137'
                InputLogin = driver.find_element_by_xpath('//*[@id="field-email"]')
                InputLogin.send_keys(login)
                InputPassword = driver.find_element_by_xpath('//*[@id="field-password"]')
                InputPassword.send_keys(password)
                ButtonLogin = driver.find_element_by_xpath('//*[@id="auth-form-login"]/div[3]/button')
                ButtonLogin.click()
                sleep(10)
        except NoSuchElementException:
            print(colored('-' * 50, 'red'))
            print(colored('Статус BotPars APPlus: OK', 'green'))
            print(colored('APPlus Login : OK', 'green'))
        #Цикл по всім сторінкам
        AllPage = 509
        i = 1
        with open ("LastPage.txt", 'r') as txt_file:
            lastPageTxtFromError = txt_file.readline()
            lastPageTxtFromError = int(lastPageTxtFromError)
        while i != lastPageTxtFromError:
            pagesErroe = driver.find_elements_by_id(f'page-{i}')
            for pageErroe in pagesErroe:
                driver.execute_script("arguments[0].click();", pageErroe)
                i = i+1
        with open ("LastPage.txt", 'r') as txt_file:
            lastPageTxt = txt_file.readline()
            lastPageTxt = int(lastPageTxt)
            while lastPageTxt <= 509:
                i = int(i)
                print(colored(f"Обробляю сторінку {i}", 'green'))
                #Підставляє сторінку в адресну строку
                pages = driver.find_elements_by_id(f'page-{i}')
                for page in pages:
                    driver.execute_script("arguments[0].click();", page)
                    #Получаєм всі Aplus номера з сторінок
                    #Отримуєм всі Aplus номера з сторінки i
                    try:
                        sleep(15)
                        waitTakeApplusNumer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="spares-table"]/tbody/tr/td[2]')))
                        TakeApplusNumer = driver.find_elements_by_xpath('//*[@id="spares-table"]/tbody/tr/td[2]')
                        with open("AllAplusNumberWihtSite.txt", "w") as txt_file:
                            for elements in TakeApplusNumer:
                                delimetr = ''
                                TakeApplusNumer = delimetr.join(elements.text)
                                txt_file.write(TakeApplusNumer)
                                txt_file.write("\n")
                                txt_file.close
                    except StaleElementReferenceException:
                        driver.execute_script("arguments[0].click();", page)
                        sleep(15)
                        waitTakeApplusNumer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="spares-table"]/tbody/tr/td[2]')))
                        TakeApplusNumer = driver.find_elements_by_xpath('//*[@id="spares-table"]/tbody/tr/td[2]')
                        sleep(2)
                        with open("AllAplusNumberWihtSite.txt", "w") as txt_file:
                            for elements in TakeApplusNumer:
                                delimetr = ''
                                TakeApplusNumer = delimetr.join(elements.text)
                                txt_file.write(TakeApplusNumer)
                                txt_file.write("\n")
                                txt_file.close
                    #Записуєм в файл всі Aplus номера (На данний момент перетворюється відразу в массив)
                    with open("AllAplusNumberWihtSite.txt", 'r+') as f:
                        AllPlusNumberWihtSite = []
                        for line in f:
                            f.truncate(0)
                            line.strip()
                            tokens = line.split("\n")
                            AllPlusNumberWihtSite.extend(tokens)
                    #Получаем товар який потрібний, з текстового файла
                    with open("TrueTovar.txt", "r") as f:
                        AllTrueTovarMass = []
                        for TrueLineTovar in f:
                            TrueLineTovar.strip()
                            tokens = TrueLineTovar.split("\n")
                            AllTrueTovarMass.extend(tokens)
                    #Порівняння двух масивів і знаходження однакових
                    VeryGoodTovar = set(AllPlusNumberWihtSite) & set(AllTrueTovarMass)
                    with open("FindNeedTovar.txt", "w") as txt_file:
                        for n in VeryGoodTovar:
                            delimetr = ''
                            FindNeedTovar = delimetr.join(n)
                            txt_file.write(FindNeedTovar)
                            txt_file.write("\n")
                            txt_file.close
                    #Записуєм в файл построчно
                    with open("FindNeedTovar.txt", 'r') as txt_file:
                        lines = txt_file.readlines()
                    #Перезаписуєм в файл построчно, щоб убрать першу пусту строку
                    with open("FindNeedTovar.txt", 'w') as txt_file:
                        txt_file.writelines(lines[1:])
                        sleep(1)
                    #Цикл по всіх товарам, які співпали 
                    with open("FindNeedTovar.txt", 'r') as txt_file:
                        for Tovar in txt_file:
                            Tovar = str(f"{Tovar}")
                            try:
                                SeacrhNeedTovar = driver.find_elements_by_class_name('product_details_link')
                            except StaleElementReferenceException:
                                SeacrhNeedTovar = driver.find_elements_by_class_name('product_details_link')
                                                            #Получаєм ссилкі на товари
                            for elements in SeacrhNeedTovar:
                                if Tovar.strip() == elements.text:
                                    print(colored(f"Товар найдений: {Tovar.strip()}, на сторінці {i}", 'green'))
                                    FindNeedTovarOK = elements.get_attribute("href")
                                    print(colored(f'Посилання на товар: {FindNeedTovarOK}', 'blue'))
                                    with open("NeedTovarUrl.txt", "a") as txt_file:
                                        txt_file.write(FindNeedTovarOK)
                                        txt_file.write("\n")
                                        txt_file.close
                i = i + 1
                with open("LastPage.txt", 'w') as txt_file:
                    i = str(i)
                    txt_file.write(i)
            else:
                print(colored('Всі сторінки перевірено!', 'green'))
        AllPars = input('Почати добавляти товар? yes/no')
        if AllPars == 'yes':
            LoginTIP = 'admin'
            passwordTIP = 'Curt_753159852'
            try:
                LoginTrue = driver.find_element_by_xpath('//*[@id="wp-admin-bar-my-account"]/a/span')
            except NoSuchElementException:
                driver.get('http://tir-rivne.com.ua/wp-login.php')
                sleep(10)
            try:
                Erroe502 = driver.find_element_by_xpath('/html/body/center[1]/h1')
                if Erroe502.is_displayed() is True:
                    print(colored('AdminPanel WordPress : 404', 'red'))
                    sleep(120)
                    BotPars()
            except NoSuchElementException:
                print(colored('AdminPanel WordPress : OK', 'green'))
                InputLoginTIP = driver.find_element_by_xpath('//*[@id="user_login"]')
                InputLoginTIP.clear()
                InputLoginTIP.send_keys(LoginTIP)
                InputPasswordTIP = driver.find_element_by_xpath('//*[@id="user_pass"]')
                InputPasswordTIP.send_keys(passwordTIP)
                SavePassword = driver.find_element_by_xpath('//*[@id="rememberme"]')
                SavePassword.click()
                ButtonLoginTIP = driver.find_element_by_xpath('//*[@id="wp-submit"]')
                ButtonLoginTIP.click()
                sleep(5)
                print(colored('WordPress Login : OK', 'green'))
            goodUrlReady = open("NeedTovarUrl.txt", "r")
            readyGoodUrl = goodUrlReady.readlines()
            for link in readyGoodUrl:
                print(colored('-' * 50, 'red'))
                driver.execute_script("window.open(arguments[0])",link)
                driver.switch_to.window(driver.window_handles[1])
                sleep(10)
                GetAPplusNumber = driver.find_element_by_class_name('urun-kodu')
                GetAPplusNumberText = GetAPplusNumber.text
                print(colored(f'Добавляю товар: {GetAPplusNumberText}', 'green'))
                GetNameTovar = driver.find_element_by_class_name('urun-basligi')
                GetNameTovarText = GetNameTovar.text
                try:
                    GetParnaDetails = driver.find_element_by_xpath('//*[@id="urun-bilgileri"]/div[3]/span/a')
                    GetTextParnaDetails = GetParnaDetails.text
                    ParnaDetails = True
                except NoSuchElementException:
                    print(colored(f'Парної деталі для товару {GetAPplusNumberText} немає!', 'red'))
                    ParnaDetails = False
                FindimgUrl = driver.find_element_by_xpath('//*[@id="urun-resmi"]/img').get_attribute('src')
                imgUrl = '{}'.format(FindimgUrl)
                img_data = requests.get(imgUrl).content
                with open(f'{GetAPplusNumberText}.jpg', 'wb') as handler:
                    handler.write(img_data)
                GetPrice = driver.find_element_by_xpath('//*[@id="spares-table"]/tbody/tr[2]/td[1]/div')
                GetPriceText = GetPrice.text
                if GetPriceText == '0.00':
                    print(colored(f'У товара {GetAPplusNumberText} немаї ціни!', 'red'))
                    GetPriceTextNone = True
                else:
                    GetPriceTextNone = False
                GetPriceTextToInt = float(GetPriceText)
                #Парсимо опис товару
                productsDetails = driver.find_elements_by_xpath('//*[@id="urun-ozellikleri-sag-kisim"]/table/tbody/tr/td')
                with open("ProductDetails.txt", 'w', encoding='utf-8') as txt_file:
                    for productDetails in productsDetails:
                        productDetails = productDetails.text
                        txt_file.write(productDetails + '\n')
                TakeOEMNumbers = driver.find_elements_by_xpath('//*[@id="urun-oem-numaralari"]/div/div[2]')
                with open("OEMNumbers.txt", 'w', encoding='utf-8') as txt_file:
                    for TakeOEMNumber in TakeOEMNumbers:
                        TakeOEMNumber = TakeOEMNumber.text
                        txt_file.write(TakeOEMNumber)
                #Перевірка наявності
                CheckAvailability = driver.find_element_by_xpath('//*[@id="spares-table"]/tbody/tr[2]/td[2]/div[1]/span')
                CheckAvailabilityText = CheckAvailability.text
                if CheckAvailabilityText == 'Під замовлення':
                    Availability = False
                    print(colored(f'Товару {GetAPplusNumberText} немає в наявності', 'red'))
                if CheckAvailabilityText != 'Під замовлення':
                    Availability = True
                    print(colored(f'Товар {GetAPplusNumberText} в наявності!', 'red'))
                driver.close()
                sleep(2)
                driver.switch_to_window(driver.window_handles[0])
                try:
                    if GetPriceTextNone == False:
                        #В боковому меню вибираємо товар
                        ButtontTovarTIP = driver.find_element_by_xpath('//*[@id="menu-posts-product"]/a/div[3]')
                        ButtontTovarTIP.click()
                        sleep(1)
                        #Додаємо новий товар
                        AddNewTovar = driver.find_element_by_xpath('//*[@id="wpbody-content"]/div[5]/a[1]')
                        AddNewTovar.click()
                        sleep(5)
                        UploadIMGButton = driver.find_element_by_xpath('//*[@id="insert-media-button"]')
                        UploadIMGButton.click()
                        #Добавляєм картинку товара
                        sleep(1)
                        UploadIMGTOVARA = driver.find_element_by_xpath('//*[@id="menu-item-featured-image"]')
                        UploadIMGTOVARA.click()
                        sleep(5)
                        imgPath = os.path.abspath(f"{GetAPplusNumberText}.jpg")
                        htm5generation = "//input[starts-with(@id,'html5_')]"
                        DownloadImg = driver.find_element_by_xpath(htm5generation)
                        DownloadImgDone = DownloadImg.send_keys(imgPath)
                        sleep(15)
                        AcceptImg = driver.find_element_by_xpath('//*[@id="__wp-uploader-id-0"]/div[4]/div/div[2]/button')
                        AcceptImg.click()
                        #Добавляєм бренд
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="in-product_brand-45"]'))).click()
                        sleep(1)
                        #Добавляєм назву товару
                        NameTovaraTIP = driver.find_element_by_xpath('//*[@id="title"]')
                        NameTovaraTIP.send_keys(GetNameTovarText)
                        #Добавляєм описання товару
                        ClickText = driver.find_element_by_xpath('//*[@id="excerpt-html"]')
                        ClickText.click()
                        sleep(1)
                        TakeTextArea = driver.find_element_by_xpath('//*[@id="excerpt"]')
                        with open('ProductDetails.txt', 'r', encoding='utf-8') as txt_file:
                            line = txt_file.readlines()
                            TakeTextArea.send_keys(line)
                        #Добавляємо парну деталь
                        if ParnaDetails == True:
                            TakeTextArea.send_keys(GetTextParnaDetails)
                        #Стандарна ціна
                        StandartPrice =  driver.find_element_by_xpath('//*[@id="_regular_price"]')
                        ForDontRegisterCliens = float(GetPriceTextToInt)
                        ForDontRegisterCliensPrice = float("{0:.2f}".format(ForDontRegisterCliens))
                        ForDontRegisterCliensPrice = str(ForDontRegisterCliensPrice)
                        StandartPrice.send_keys(ForDontRegisterCliensPrice)
                        #Ціна зі скидкой
                        DiscountPrice = driver.find_element_by_xpath('//*[@id="_sale_price"]')
                        ForRegisterCliens = float((GetPriceTextToInt/100)*60)
                        ForRegisterCliensPrice = float("{0:.2f}".format(ForRegisterCliens))
                        ForRegisterCliensPrice = str(ForRegisterCliensPrice)
                        DiscountPrice.send_keys(ForRegisterCliensPrice)
                        #Добавляєм тег
                        AddTags = driver.find_element_by_xpath('//*[@id="new-tag-product_tag"]')
                        AddTags.send_keys('APPlus')
                        ClickAddTags = driver.find_element_by_xpath('//*[@id="product_tag"]/div/div[2]/input[2]')
                        ClickAddTags.click()
                        #Добавляєм наявність
                        if Availability == True:
                            #Наявність Рівне
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="acf-field_6048bb2f118ca"]'))).click()
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acf-field_6048bb2f118ca"]/option[1]'))).click()
                            sleep(1)
                            #Наявність Камянець-Подільський
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="acf-field_6048be07d3019"]'))).click()
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acf-field_6048be07d3019"]/option[1]'))).click()
                            sleep(1)
                            #Наявність Рівне-РЦ
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="acf-field_6048be14d301a"]'))).click()
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acf-field_6048be14d301a"]/option[1]'))).click()
                            sleep(1)
                            #Наявність Київ-РЦ
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="acf-field_6087ec1886d50"]'))).click()
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acf-field_6087ec1886d50"]/option[1]'))).click()
                        if Availability == False:
                            #Наявність Рівне
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="acf-field_6048bb2f118ca"]'))).click()
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acf-field_6048bb2f118ca"]/option[8]'))).click()
                            sleep(1)
                            #Наявність Камянець-Подільський
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="acf-field_6048be07d3019"]'))).click()
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acf-field_6048be07d3019"]/option[8]'))).click()
                            sleep(1)
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="acf-field_6048be14d301a"]'))).click()
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acf-field_6048be14d301a"]/option[8]'))).click()
                            sleep(1)
                            #Наявність Київ-РЦ
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="acf-field_6087ec1886d50"]'))).click()
                            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acf-field_6087ec1886d50"]/option[8]'))).click()
                            sleep(1)
                        #Добавляємо APPlus номер
                        ClickAvaibility = driver.find_element_by_xpath('//*[@id="woocommerce-product-data"]/div[2]/div/ul/li[2]/a/span')
                        ClickAvaibility.click()
                        InputAPPlusNomer = driver.find_element_by_xpath('//*[@id="_sku"]')
                        InputAPPlusNomer.send_keys(GetAPplusNumberText)
                        #Добавляєм OEM номера 
                        InputOEMNumers = driver.find_element_by_xpath('//*[@id="jk_sku1"]')
                        file = open('OEMNumbers.txt', 'r', encoding='utf-8')
                        num = ''
                        for line in file.readlines():
                            num += line
                        num = num.replace('\n',' ')
                        InputOEMNumers.send_keys(num)
                        sleep(2)
                        PublicTovar = driver.find_element_by_id('publish')
                        driver.execute_script("arguments[0].click();", PublicTovar)
                        sleep(10)
                        print(colored(f'Товар {GetAPplusNumberText} успішно добавлений!', 'green'))
                        print(colored('-' * 50, 'red'))
                    elif GetPriceTextNone == True:
                        print(colored(f"Товар: {GetAPplusNumberText} не буде добавлений, тому що в нього немає ціни!", 'red'))
                        with open('NeedTovarUrl.txt', 'r+', encoding='utf-8') as txt_file:
                            data = txt_file.read().splitlines(True)
                            txt_file.truncate(0)
                            txt_file.writelines(data[1:])
                            driver.close()
                            BotPars()
                except NoSuchElementException:
                        print(colored('ALARM!!! ERROR 404 !!!', 'red'))
            print(colored('Весь товар успішно добавлений!', 'green'))
            sleep(1000)
    init()
    BotPars()
    sleep(1000)
