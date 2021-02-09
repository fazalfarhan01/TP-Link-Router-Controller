from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep


class TP_Link_Controller():
    def __init__(self,login_email, login_password, router_url = "192.168.0.1", driver_path = "./bin/chromedriver.exe"):
        # VARIABLES
        self.driver_path = driver_path
        self.admin_panel_url = "http://"+ router_url +"/"
        self.email = login_email
        self.password = login_password
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

    def login(self):
        self.driver.get(self.admin_panel_url)
        self.driver.implicitly_wait(30)

        email_box = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div/form[1]/div[1]/div/div/div[1]/span[4]/input")
        email_box.click()
        email_container = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div/form[1]/div[1]/div/div/div[1]/span[2]/input")
        email_container.send_keys(self.email)
        email_container.send_keys(Keys.RETURN)

        password_box = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div/form[1]/div[2]/div/div/div[1]/span[3]/input")
        password_box.click()
        password_container = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div/form[1]/div[2]/div/div/div[1]/span[2]/input[1]")
        password_container.send_keys(self.password)
        password_container.send_keys(Keys.RETURN)
    
    def toggle_2g_wifi(self):
        wireless_tab_button = self.driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[1]/ul/li[3]/a/span[2]")
        wireless_tab_button.click()

        # Waiting for loading to complete
        sleep(5)
        
        enable_wireless_radio_2_4G = self.driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[1]/div[2]/div[1]/ul/li/div/label/span[2]")
        enable_wireless_radio_2_4G.click()

        save_button = self.driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[9]/div/div/div/div[1]/button")
        save_button.click()

    def toggle_5g_wifi(self):
        wireless_tab_button = self.driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[1]/ul/li[3]/a/span[2]")
        wireless_tab_button.click()
        
        # Waiting for loading to complete
        sleep(5)

        enable_wireless_radio_5G = self.driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[5]/div[2]/div[1]/ul/li/div/label")
        enable_wireless_radio_5G.click()

        save_button = self.driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[9]/div/div/div/div[1]/button")
        save_button.click()

    def close(self):
        # waiting explicitly for 5 seconds
        print("Waiting explicitly for 5 seconds brfore closing")
        sleep(5)
        self.driver.close()

if __name__ == "__main__":
    controller = TP_Link_Controller("fazal.farhan@gmail.com", "mohamedfarhan12")
    controller.login()
    # controller.toggle_2g_wifi()
    controller.toggle_5g_wifi()
    controller.close()