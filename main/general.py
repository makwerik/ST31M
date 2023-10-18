import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from twocaptcha import wrapper
import undetected_chromedriver as uc
from options_driver import *


class SteamHelpWithLoginInfo:
    """
    Класс для восстановления паролей STEAM
    """

    def __init__(self, api_key=None, site_key=None, url=None, num=None):
        """
        Инициализатор браузера/настроек браузера/юзер-агентов/класс для решения капчи
        :param api_key: Ключ из аккаунта Rucaptcha
        :param site_key: Ключ сайта с капчей
        :param url: Ссылка на сайт с капчей
        :param num: Номер телефона
        """

        self.driver = uc.Chrome(options=options)
        self.solver = wrapper.TwoCaptcha(api_key)
        self.api_key = api_key
        self.site_key = site_key
        self.url = url
        self.num = num
        self.count = 0

    def connecting_to_the_site(self):
        """
        Переход на сайт для восстановления пароля.
        В случае неудачи 3 попытки повторного подключения с интервалом 3 секунды
        """
        try:

            self.driver.get("https://help.steampowered.com/ru/wizard/HelpWithLoginInfo?issueid=406")
            print('Подключение к сайту: Успешно!')
            self.count = 0
            self.__entering_number()
        except:
            self.count += 1
            print(f'Не удалость зайти на сайт: https://help.steampowered.com/ru/wizard/HelpWithLoginInfo?issueid=406 \n'
                  f'Попытка переподключения №{self.count}')
            if self.count < 3:
                time.sleep(3)
                self.connecting_to_the_site()

    def __entering_number(self):
        """
        Ввод номера телефона на сайте, переключение на фрайм для решения капчи
        """
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#forgot_login_search').send_keys('8' + self.num)
            self.__solver_captcha_extension()
        except:
            print('Не удалось ввести номер телефона')
            print('Начинаю сначала')
            self.connecting_to_the_site()

    def __solver_captcha(self):
        """
        Решаем капчу
        """
        print('Решаю капчу')
        try:
            result = self.solver.solve_captcha(page_url=self.url, site_key=self.site_key)

            self.driver.execute_script("arguments[0].value = arguments[1]",
                                       self.driver.find_element(By.CSS_SELECTOR, "textarea"), result)
            print('Капча решена')
            time.sleep(3)
            self.__check_box()
        except:
            print('Не удалось решить капчу. Проверьте баланс аккаунта')
            print('Начинаю выполнение скрипта заново...')
            self.connecting_to_the_site()

    def __solver_captcha_extension(self):
        """
        Решаем капчу с помощью расширения от рукапчи
        """
        WebDriverWait(self.driver, 30).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'captcha-solver-info'), 'Решить с 2Captcha'))
        self.driver.find_element(By.CLASS_NAME, 'captcha-solver').click()

        WebDriverWait(self.driver, 300).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'captcha-solver-info'), 'Капча решена!'))
        self.__check_box()

    def __check_box(self):
        try:
            iframe = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
            self.driver.switch_to.frame(iframe)
            self.driver.find_element(By.CSS_SELECTOR, '#recaptcha-anchor > div.recaptcha-checkbox-border').click()
            self.driver.switch_to.default_content()
            self.driver.find_element(By.CSS_SELECTOR, '#forgot_login_search_form > div.account_recovery_submit > '
                                                      'input[type=submit]').click()
            self.__find_account()
        except:
            print('Не получилось пройти проверку')
            self.connecting_to_the_site()

    def __find_account(self):
        """
        Получаем информацию о найденом аккаунте (до конца не тестил, может давать сбои)
        """
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#wizard_contents > div > a:nth-child(5) > span'))
            )

            self.driver.find_element(By.XPATH, f"//*[contains(text(), 'Мы нашли аккаунт, связанный с «+7{self.num}»')]")
            with open(f'data/result.txt', 'a', encoding='utf8') as find_done:
                find_done.write('8' + self.num)
            print('Аккаунт найден')
        except:
            print('Аккаунт не найден')


if __name__ == '__main__':
    with open('numbers.csv') as file:
        number = file.readlines()
    for n in number:
        steam = SteamHelpWithLoginInfo(api_key='',
                                       site_key='',
                                       url='https://help.steampowered.com/ru/wizard/HelpWithLoginInfo?issueid=406',
                                       num=n)
        steam.connecting_to_the_site()
        steam.driver.quit()
