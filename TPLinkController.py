#!/usr/bin/python3

from os import SEEK_CUR
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep
from sys import platform
from browsermobproxy import Server
import json
import re


from colorama import init, Fore, Back, Style

reset = Style.RESET_ALL
error = Fore.RED + "Error: " + reset
info = Fore.LIGHTCYAN_EX + "Info: " + reset
warning = Fore.LIGHTYELLOW_EX + "Warning: " + reset
title = Fore.BLACK + Back.GREEN


class TP_Link_Controller():
    def __init__(self,
                 login_email,
                 login_password,
                 router_url="192.168.0.1",
                 driver_path="./bin/chromedriver.exe",
                 browsermobproxy_location=r"bin\browsermob-proxy-2.1.4\bin\browsermob-proxy",
                 DEBUG_MODE=False):
        # VARIABLES
        self.driver_path = self.__get_driver_path(driver_path)
        self.proxy_path = browsermobproxy_location
        self.admin_panel_url = "http://" + router_url + "/"
        self.email = login_email
        self.password = login_password
        self.DEBUG_MODE = DEBUG_MODE
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.headless = True

        self.server = Server(browsermobproxy_location)
        self.server.start()
        self.proxy = self.server.create_proxy()

        options.add_argument('--proxy-server=%s' % self.proxy.proxy)

        self.driver = webdriver.Chrome(
            executable_path=self.driver_path, options=options)
        self.driver.implicitly_wait(30)
        if DEBUG_MODE:
            print(info + "Driver Path:\t{}".format(self.driver_path))
            print(info + "Admin Panel URL:\t{}".format(self.admin_panel_url))
            print(info + "Login Email:\t{}".format(self.email))
            print(info + "Login Password:\t{}".format(self.password))

    def __get_driver_path(self, path):
        # RETURN THE DEFAULT PATH OF CHROME DRIVER FOR LINUX
        if platform == "linux":
            return "/usr/bin/chromedriver"
        else:
            return path

    def __wait_for_data(self, xpath, attribute="snapshot", value=None):
        sleep(2)
        # ignored_exceptions = (NoSuchElementException,
        #                       StaleElementReferenceException,)
        # dummay_element = WebDriverWait(self.driver, 30, ignored_exceptions=ignored_exceptions)\
        #     .until(EC.presence_of_element_located((By.XPATH, xpath)))
        # LOOP UNTIL THE ELEMENT ATTRIBUTE IS NOT "None"
        if value == None:
            while self.driver.find_element_by_xpath(xpath).get_attribute(attribute) is value:
                pass
        else:
            while value not in self.driver.find_element_by_xpath(xpath).get_attribute(attribute):
                pass

    def __click_save(self):
        # THE SAVE BUTTON IN THE WEBPAGE WHICH HAS A COMMON ID AS id="total_save"
        if self.DEBUG_MODE:
            print(info + "Clicking on Save.")
        # self.driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[9]/div/div/div/div[1]/button").click()
        self.driver.find_element_by_id("total_save").click()

    def __get_stok(self, data_url="http://192.168.0.1/webpages/index.1516243669548.html"):
        # RETURNS THE STOK THAT IS RENEWED AFTER EVERY LOGIN ATTEMPT
        # FOR EXAMPLE IN THE URL http://router.login/cgi-bin/luci/;stok=dda6af0b1901e48c9ce10d115f287dcd/admin/status?form=all
        # dda6af0b1901e48c9ce10d115f287dcd IS THE STOK
        self.proxy.new_har("STOK")
        self.driver.get(data_url)
        self.__wait_for_data(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/form/div[1]/div[1]/div[1]/div[2]/div[1]/span[2]/input", "snapshot")
        entries = self.proxy.har['log']["entries"]
        for entry in entries:
            if 'request' in entry.keys():
                url = entry['request']['url']
                if url.startswith("http://192.168.0.1/cgi-bin/luci/;stok=") and "admin" in url:
                    stok = re.findall("([a-zA-z0-9]+)/", entry['request']['url'].replace(
                        "http://192.168.0.1/cgi-bin/luci/;stok=", ""))
                    return stok[0]

    def login(self):
        self.driver.get(self.admin_panel_url)
        if self.DEBUG_MODE:
            print(title + "Logging In...!" + reset)
        # sleep(5)
        if self.DEBUG_MODE:
            print(info + "Page Title:\t{}".format(self.driver.title))
            print(info + "Entering Email:\t{}".format(self.email))

        email_box = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div[1]/div[1]/div/form[1]/div[1]/div/div/div[1]/span[4]/input")
        email_box.click()
        email_container = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div[1]/div[1]/div/form[1]/div[1]/div/div/div[1]/span[2]/input")
        email_container.send_keys(self.email)
        email_container.send_keys(Keys.RETURN)

        if self.DEBUG_MODE:
            print(info + "Entering Password:\t{}".format(self.password))

        password_box = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div[1]/div[1]/div/form[1]/div[2]/div/div/div[1]/span[3]/input")
        password_box.click()
        password_container = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div[1]/div[1]/div/form[1]/div[2]/div/div/div[1]/span[2]/input[1]")
        password_container.send_keys(self.password)
        password_container.send_keys(Keys.RETURN)
        self.__wait_for_data(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/form/div[1]/div[1]/div[1]/div[2]/div[1]/span[2]/input", "snapshot")

    def toggle_2g_wifi(self):
        if self.DEBUG_MODE:
            print(title + "Toggling 2G WiFi" + reset)

        if self.DEBUG_MODE:
            print(info + "Clicking on Wireless Section")
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[1]/ul/li[3]/a/span[2]").click()

        # Waiting for loading to complete
        if self.DEBUG_MODE:
            print(info + "Waiting for data to load.")

        self.__wait_for_data(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/div[1]/span[2]/input")

        if self.DEBUG_MODE:
            print(info + "Toggling 2.4G WiFi Checkbox")
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[1]/div[2]/div[1]/ul/li/div/label/span[2]").click()

        self.__click_save()
        self.__wait_for_save_confirmation_on_wireless_tab()

    def toggle_5g_wifi(self):
        if self.DEBUG_MODE:
            print(title + "Toggling 5G WiFi" + reset)

        if self.DEBUG_MODE:
            print(info + "Clicking on Wireless Section")
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[1]/ul/li[3]/a/span[2]").click()

        if self.DEBUG_MODE:
            print(info + "Waiting for data to load.")

        # Looping until data pops up
        self.__wait_for_data(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/div[1]/span[2]/input")

        if self.DEBUG_MODE:
            print(info + "Toggling 5G WiFi Checkbox")
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[5]/div[2]/div[1]/ul/li/div/label").click()

        self.__click_save()
        self.__wait_for_save_confirmation_on_wireless_tab()

    def __get_json_status_data(self, stok):
        data_url = self.admin_panel_url + \
            "cgi-bin/luci/;stok="+stok+"/admin/status?form=all"
        self.driver.get(data_url)
        json_response = json.loads(
            self.driver.find_element_by_xpath("/html/body/pre").text)
        # print(json_response)
        return json_response

    def get_status(self):
        stok = self.__get_stok()
        response = self.__get_json_status_data(stok)
        self.driver.back()
        return response

    def turn_on_5G(self):
        if self.DEBUG_MODE:
            print(title + "Turning on 5G WiFi" + reset)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[1]/ul/li[3]/a/span[2]").click()
        if self.DEBUG_MODE:
            print(info + "Clicking on Wireless Section")

        if self.DEBUG_MODE:
            print(info + "Waiting for data to load.")

        # Looping until data pops up
        self.__wait_for_data(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/div[1]/span[2]/input")

        WiFi_5G_Checkbox = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[5]/div[2]/div[1]/ul/li/div/label")
        if "checked" in WiFi_5G_Checkbox.get_attribute("class"):
            print(warning + "5G WiFi Already On")
            self.__click_save()
        else:
            print(info + "Clicking on 5G WiFi Checkbox (Turning On)")
            WiFi_5G_Checkbox.click()
            self.__click_save()
        self.__wait_for_save_confirmation_on_wireless_tab()

    def turn_off_5G(self):
        if self.DEBUG_MODE:
            print(title + "Turning off 5G WiFi" + reset)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[1]/ul/li[3]/a/span[2]").click()
        if self.DEBUG_MODE:
            print(info + "Clicking on Wireless Section")

        if self.DEBUG_MODE:
            print(info + "Waiting for data to load.")

        # Looping until data pops up
        self.__wait_for_data(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/div[1]/span[2]/input")

        WiFi_5G_Checkbox = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[5]/div[2]/div[1]/ul/li/div/label")
        if "checked" not in WiFi_5G_Checkbox.get_attribute("class"):
            print(warning + "5G WiFi Already Off")
            self.__click_save()
        else:
            print(info + "Clicking on 5G WiFi Checkbox (Turning Off)")
            WiFi_5G_Checkbox.click()
            self.__click_save()
        self.__wait_for_save_confirmation_on_wireless_tab()

    def turn_on_2G(self):
        if self.DEBUG_MODE:
            print(title + "Turning on 5G WiFi" + reset)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[1]/ul/li[3]/a/span[2]").click()
        if self.DEBUG_MODE:
            print(info + "Clicking on Wireless Section")

        if self.DEBUG_MODE:
            print(info + "Waiting for data to load.")

        # Looping until data pops up
        self.__wait_for_data(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/div[1]/span[2]/input")

        WiFi_2G_Checkbox = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[1]/div[2]/div[1]/ul/li/div/label")
        if "checked" in WiFi_2G_Checkbox.get_attribute("class"):
            print(warning + "2G WiFi Already On")
            self.__click_save()
        else:
            print(info + "Clicking on 2G WiFi Checkbox (Turning On)")
            WiFi_2G_Checkbox.click()
            self.__click_save()
        self.__wait_for_save_confirmation_on_wireless_tab()

    def turn_off_2G(self):
        if self.DEBUG_MODE:
            print(title + "Turning off 5G WiFi" + reset)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[1]/ul/li[3]/a/span[2]").click()
        if self.DEBUG_MODE:
            print(info + "Clicking on Wireless Section")

        if self.DEBUG_MODE:
            print(info + "Waiting for data to load.")

        # Looping until data pops up
        self.__wait_for_data(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/div[1]/span[2]/input")

        WiFi_2G_Checkbox = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[1]/div[2]/div[1]/ul/li/div/label")
        if "checked" not in WiFi_2G_Checkbox.get_attribute("class"):
            print(warning + "2G WiFi Already Off")
            self.__click_save()
        else:
            print(info + "Clicking on 2G WiFi Checkbox (Turning Off)")
            WiFi_2G_Checkbox.click()
            self.__click_save()
        self.__wait_for_save_confirmation_on_wireless_tab()

    def is_2g_on(self):
        if self.DEBUG_MODE:
            print(title + "Getting 2.4G WiFi Status" + reset)
        status_response = self.get_status()
        if self.DEBUG_MODE:
            print(
                info + "Got 2.4G WiFi Status: {}".format(status_response["data"]["wireless_2g_enable"]))
        if status_response["data"]["wireless_2g_enable"] == "on":
            return True
        else:
            return False

    def is_5g_on(self):
        if self.DEBUG_MODE:
            print(title + "Getting 5G WiFi Status" + reset)
        status_response = self.get_status()
        if self.DEBUG_MODE:
            print(
                info + "Got 5G WiFi Status: {}".format(status_response["data"]["wireless_2g_enable"]))
        if status_response["data"]["wireless_5g_enable"] == "on":
            return True
        else:
            return False

    def __wait_for_save_confirmation_on_wireless_tab(self):
        if self.DEBUG_MODE:
            print(info + "Waiting for save confirmation.")
        confirmation_logo_x_path = "/html/body/div[1]/div[5]/div[1]/div[1]/div/div/div[2]/div/div[1]/div/div[2]/div[2]/form/div[10]"
        self.__wait_for_data(confirmation_logo_x_path, attribute="style", value="block")
        if self.DEBUG_MODE:
            print(info + "Save confirmation opened..!")
        self.__wait_for_data(confirmation_logo_x_path, attribute="style", value="none")
        if self.DEBUG_MODE:
            print(info + "Save confirmation closed..!")

    def close(self):
        # waiting explicitly for 5 seconds
        if self.DEBUG_MODE:
            print(warning + "Waiting explicitly for 5 seconds brfore closing")
        sleep(5)

        self.server.stop()
        self.driver.close()
        # self.driver.quit()


if __name__ == "__main__":
    controller = TP_Link_Controller(
        "fazal.farhan@gmail.com", "mohamedfarhan12", DEBUG_MODE=True)

    controller.login()

    controller.get_status()

    # controller.close()
