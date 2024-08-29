import time

from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
import pandas as pd

from bs4 import BeautifulSoup


def scraper():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome()

    driver.get('https://racenet.com/')

    time.sleep(3)
    
    button_clicker(driver, ('id', 'truste-consent-button'))

    driver.find_element(By.XPATH, "//button[text()='SIGN IN']").click()

    username = '$USERNAME'
    password_racenet = '$PASSWORD'

    driver.find_element('id', 'email').send_keys(username)
    driver.find_element('id', 'password').send_keys(password_racenet)

    button_clicker(driver, ('id', 'logInBtn'))

    button_clicker(driver, ('id', 'btnSendCode'))

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://poczta.wp.pl/")

    password_mail = '$PASSWORD'

    button_clicker(driver, (By.XPATH, "//button[text()='AKCEPTUJĘ I PRZECHODZĘ DO SERWISU']"))

    driver.find_element('id', 'login').send_keys(username)
    driver.find_element('id', 'password').send_keys(password_mail)

    button_clicker(driver, (By.XPATH, "//button[text()='Zaloguj się']"))

    time.sleep(15)

    code = driver.find_element(By.XPATH, "//div[contains(text(), 'Twój kod bezpieczeństwa EA')]").text.split(" ")[-1]

    driver.close()

    driver.switch_to.window(driver.window_handles[0])

    driver.find_element('id', 'twoFactorCode').send_keys(code)

    button_clicker(driver, ('id', 'btnSubmit'))

    time.sleep(3)

    driver.get(
        'https://racenet.com/f1_23/performanceAnalysis/player?trackId=27&mode=00&weather=D&version=1&isCrossPlay=true')

    button_clicker(driver, (By.XPATH, "//button[text()='Ok']"))

    time.sleep(5)

    html = driver.execute_script("return document.documentElement.innerHTML;")

    driver.close()

    bs = BeautifulSoup(html, 'html.parser')

    records = bs.find_all('ul', {"class": 'MuiList-root MuiMenu-list MuiList-padding'})

    res = []

    for li in records:
        res.extend(li.find_all_next('li', {"class": 'MuiButtonBase-root MuiListItem-root MuiMenuItem-root '
                                                    'MuiMenuItem-gutters MuiListItem-gutters MuiListItem-button',
                                           'aria-disabled': 'false'}))

    results = []

    for x in res:
        try:
            nick = x.find_next('p', {
                'class': re.compile('MuiTypography-root jss[0-9][0-9][0-9][0-9] MuiTypography-body1')}).text
            if nick == 'Max Verstappen':
                continue
            date = x.find_next('p', {'class': 'MuiTypography-root MuiTypography-body1 MuiTypography-alignRight'}).text
            laptime = x.find_next('p', {'class': 'MuiTypography-root MuiTypography-body1 MuiTypography-alignLeft'}).text
            results.append({'nick': nick, 'date': date, 'time': laptime})
        except AttributeError:
            continue

    df = pd.DataFrame(results)

    return df.drop_duplicates()


def button_clicker(driver, element):
    try:
        link = WebDriverWait(driver, 20).until(ec.element_to_be_clickable(element))
        link.click()
    except ElementClickInterceptedException:
        print("Trying to click on the button again")
        driver.execute_script("arguments[0].click()", link)
