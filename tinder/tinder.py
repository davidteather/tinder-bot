from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth

import time


class Tinder:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        # options.add_argument("--headless")

        options.add_experimental_option(
            "prefs",
            {
                "profile.default_content_setting_values.geolocation": 1,
                "profile.password_manager_enabled": False,
                "credentials_enable_service": False
            },
        )

        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=options)

        # Madison, WI Coords
        coords = {
            "latitude": 43.073051,
            "longitude": -89.40123,
            "accuracy": 98,
        }

        self.driver.execute_cdp_cmd("Page.setGeolocationOverride", coords)

        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    def __handle_homescreen_popup(self):
        try:
            add_tinder_to_homescreen = self.driver.find_elements_by_xpath(
                "//button[@data-testid='addToHomeScreen']/parent::*/button")[1]
            add_tinder_to_homescreen.click()
        except:
            pass

    def __handle_no_more_matches(self):
        try:
            i = self.driver.find_elements_by_xpath("//div[@class='Pos(a) B(20px) Ta(c) C($c-secondary) Px(28px) Fz($s)']")
            if len(i) != 0:
                item = i[0]
                if "unable to find any potential matches" in item.text.strip().lower():
                    self.driver.refresh()
        except:
            pass

    def login_google(self, username, password):
        url = ("https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?redirect_uri=storagerelay"
               "%3A%2F%2Fhttps%2Ftinder.com%3Fid%3Dauth133997&response_type=permission id_token&scope=email "
               "profile openid&openid.realm&client_id=230402993429-g4nobau40t3v3j0tvqto4j8f35kil4hf.apps.go"
               "ogleusercontent.com&ss_domain=https%3A%2F%2Ftinder.com&fetch_basic_profile=true&gsiwebsdk=2&flowName=GeneralOAuthFlow")

        self.driver.get(url)
        time.sleep(1)

        email_or_phone = self.driver.find_element_by_xpath(
            "//input[@type='email']")
        email_or_phone.send_keys(username)
        time.sleep(1.3)

        next_button = self.driver.find_elements_by_xpath("//button")[3]
        next_button.click()
        time.sleep(2)

        password_box = self.driver.find_element_by_xpath(
            "//input[@name='password']")
        password_box.send_keys(password)
        time.sleep(2)
        next_button = self.driver.find_elements_by_xpath("//button")[1]
        next_button.click()

        input("Please login with google \n")

        url = "https://tinder.com/"
        self.driver.get(url)
        time.sleep(1)
        login_btn = self.driver.find_element_by_xpath(
            "//span[@class='Pos(r) Z(1)']")
        login_btn.click()
        time.sleep(1)

        google_login = self.driver.find_elements_by_xpath(
            "//span[@class='Pos(r) Z(1) D(ib)']"
        )[0]
        google_login.click()
        time.sleep(5)

        allow_geolocation = self.driver.find_element_by_xpath(
            "//button[@aria-label='Allow']"
        )
        allow_geolocation.click()
        time.sleep(0.3)

        deny_notifications = self.driver.find_element_by_xpath(
            "//button[@aria-label='Not interested']"
        )
        deny_notifications.click()
        time.sleep(0.3)

    def login(self, phone_number, cookies=None):
        url = "https://tinder.com/"
        self.driver.get(url)
        time.sleep(1)
        login_btn = self.driver.find_element_by_xpath(
            "//span[@class='Pos(r) Z(1)']")
        login_btn.click()
        time.sleep(1)

        phone_number_box = self.driver.find_elements_by_xpath(
            "//span[@class='Pos(r) Z(1) D(ib)']"
        )[2]
        phone_number_box.click()
        time.sleep(0.3)

        input_number = self.driver.find_element_by_xpath(
            "//input[@name='phone_number']"
        )
        input_number.send_keys(phone_number)
        time.sleep(0.3)

        continue_button = self.driver.find_elements_by_xpath(
            "//button[@type='button']"
        )[4]
        continue_button.click()

        verify_code = input("Enter your verification number on phone\n")

        verification_boxes = self.driver.find_elements_by_xpath(
            "//input[@type='tel']")
        for x in range(len(verification_boxes)):
            box = verification_boxes[x]
            box.send_keys(verify_code[x])

        continue_button = self.driver.find_elements_by_xpath(
            "//button[@type='button']"
        )[4]
        continue_button.click()

        verify_code = input("Enter your verification number from email\n")

        verification_boxes = self.driver.find_elements_by_xpath(
            "//input[@type='tel']")
        for x in range(len(verification_boxes)):
            box = verification_boxes[x]
            box.send_keys(verify_code[x])

        continue_button = self.driver.find_elements_by_xpath(
            "//button[@type='button']"
        )[4]
        continue_button.click()
        time.sleep(1)

        allow_geolocation = self.driver.find_element_by_xpath(
            "//button[@aria-label='Allow']"
        )
        allow_geolocation.click()
        time.sleep(0.3)

        deny_notifications = self.driver.find_element_by_xpath(
            "//button[@aria-label='Not interested']"
        )
        deny_notifications.click()
        time.sleep(0.3)

    def dislike(self):
        skip_button = self.driver.find_elements_by_xpath(
            "//div[@class='Pos(r) Py(16px) Py(12px)--s Px(4px) Px(8px)--ml D(f) Jc(sb) Ai(c) Maw(375px)--m Mx(a) Pe(n) Mt(-1px)']/div/button"
        )[1]
        skip_button.click()
        time.sleep(0.3)

        self.__handle_no_more_matches()
        self.__handle_homescreen_popup()
        

    def like(self):
        like_button = self.driver.find_elements_by_xpath(
            "//div[@class='Pos(r) Py(16px) Py(12px)--s Px(4px) Px(8px)--ml D(f) Jc(sb) Ai(c) Maw(375px)--m Mx(a) Pe(n) Mt(-1px)']/div/button"
        )[2]
        like_button.click()
        time.sleep(0.3)

        self.__handle_no_more_matches()
        self.__handle_homescreen_popup()
        

    def extract_current(self):
        main_card = self.driver.find_elements_by_xpath(
            "//span[@class='keen-slider__slide Wc($transform) Fxg(1)']/div"
        )[1]

        name = main_card.get_attribute("aria-label")
        # main_image = main_card.get_attribute('style').split("url(")[1].split("\");")[0]

        bio_wrapper = self.driver.find_elements_by_xpath("//div[@aria-hidden='false' and @class='Toa(n) Wc($transform) Prs(1000px) Bfv(h) Ov(h) W(100%) StretchedBox Bgc($c-placeholder) Bdrs(8px)']/div[@tabindex='0']/div[@class='Tsh($tsh-s) D(f) Fx($flx1) Fxd(c) Miw(0)']/div/div/div[@class='BreakWord Whs(pl) Fz($ms) Ta(start) Animn($anim-slide-in-left) Animdur($fast) LineClamp(5,118.125px)']"
                                                         )

        if len(bio_wrapper) == 0:
            bio = None
        else:
            bio = bio_wrapper[0].text

        image_count = len(
            self.driver.find_elements_by_xpath(
                "//div[@aria-hidden='false']/div/div[@class='CenterAlign D(f) Fxd(r) W(100%) Px(8px) Pos(a) TranslateZ(0)']/button"
            )
        )
        images = []

        body = self.driver.find_element_by_xpath("//body")
        for i in range(image_count+2):
            image = (
                self.driver.find_elements_by_xpath(
                    f"//div[@class='Expand Pos(a) D(f) Ov(h) Us(n) keen-slider']/span/div[@aria-label='{name}']"
                )[0]
                .get_attribute("outerHTML")
                .split("url(&quot;")[1]
                .split('&quot;);')[0]
            )
            if image not in images:
                images.append(image)
            body.send_keys(Keys.SPACE)
            time.sleep(0.3)

        return {"name": name, "bio": bio, "images": images}

    def slide_current(self):
        e = self.driver.find_element_by_xpath("//div[@aria-live='polite']")
        move = ActionChains(self.driver)
        move.click_and_hold(e).move_by_offset(20, 0).release().perform()

    def exit(self):
        self.driver.quit()
