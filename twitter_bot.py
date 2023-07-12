import os
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

PROMISED_DOWN = 3000
PROMISED_UP = 750
TWITTER_EMAIL = os.environ['TWITTER_EMAIL']
TWITTER_PASSWORD = os.environ['TWITTER_PASSWORD']


class InternetSpeedTwitterBot:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.service = Service(executable_path="C:\ChromeDriver-for-Selenium\chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service, chrome_options=self.chrome_options)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")

        privacy_acceptation_window = self.driver.find_element(by=By.ID, value="onetrust-accept-btn-handler")
        privacy_acceptation_window.click()

        sleep(2)

        start_button = self.driver.find_element(by=By.CLASS_NAME, value="start-text")
        start_button.click()

        sleep(40)

        actions = ActionChains(self.driver)
        close_button = self.driver.find_element(by=By.CLASS_NAME, value="close-btn")
        actions.move_to_element(close_button).click().perform()

        self.down = float(self.driver.find_element(by=By.CLASS_NAME, value="download-speed").text)
        self.up = float(self.driver.find_element(by=By.CLASS_NAME, value="upload-speed").text)

        print(f"Measured download:{self.down}Mbit/s, upload:{self.up}Mbit/s")

        if self.up < PROMISED_UP or self.down < PROMISED_DOWN:
            complain_needed = input(f"Would you like to tweet complain? (Y/N)\n")
            while complain_needed != "y" and complain_needed != "n":
                complain_needed = input(f"Please answer with Y or N...\n")
            if complain_needed == "y":
                self.tweet_at_provider(up=self.up, down=self.down)
            else:
                print((f"Your complain could have been tweeted like this:\n"
                       f"Dear DIGI, could you please clarify for me, why is my internet speed only {self.down}/{self.up}Mbit/s "
                       f"(down/up) instead of the minimum guaranteed {PROMISED_DOWN}/{PROMISED_UP}Mbit/s 😒? Many thanks!"))

    def tweet_at_provider(self, up, down):
        self.driver.get("https://twitter.com/")

        try:
            sleep(2)
            login_button = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/a/div/span/span')
            login_button.click()

            sleep(2)

            email_input = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
            email_input.send_keys(TWITTER_EMAIL)

            next_button = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')

            next_button.click()

            sleep(2)

            password_input = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
            password_input.send_keys(TWITTER_PASSWORD)

            login_button = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
            login_button.click()

            sleep(3)

            text_area = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
            text_area.send_keys(f"Dear DIGI, could you please clarify for me, why is my internet speed only {down}/{up}Mbit/s "
                                f"(down/up) instead of the minimum guaranteed {PROMISED_DOWN}/{PROMISED_UP}Mbit/s 😒? Many thanks!")

            tweet_button = self.driver.find_element(by=By.XPATH,
                                                    value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[3]/div/span/span')
            tweet_button.click()


        except NoSuchElementException:
            print(f"Some elements were missing. Should have complained like:\n"
                  f"Dear DIGI, could you please clarify for me, why is my internet speed only {down}/{up}Mbit/s "
                  f"(down/up) instead of the minimum guaranteed {PROMISED_DOWN}/{PROMISED_UP}Mbit/s 😒? Many thanks!")




