from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from random import randint
import time 
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from captcha_bypass import solveCaptcha_pro
import randominfo as ri
import zipfile


# usera = open('user_agents.txt', 'r')
# ua = usera.read()
# user_agents = ua.splitlines()

proxy_file = open('proxies.txt', 'r')
proxies = proxy_file.read()
proxies_list = proxies.splitlines()

use_p = open('use_proxy.txt', 'r')
is_proxy = use_p.read() 


def changeproxy():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension('ext.crx')
    
    pluginfile = 'proxy_auth_plugin.zip'
    
    if is_proxy == 'True' or is_proxy == 'true':
        
        total_proxies = len(proxies_list)
        select_proxy = proxies_list[randint(1, total_proxies-1)]
        proxy = select_proxy.split(':')

        # total_ua = len(user_agents)
        # user_agent = user_agents[randint(1, total_ua-1)]

        PROXY_HOST = proxy[0]
        PROXY_PORT = int(proxy[1])
        PROXY_USER = proxy[2] # username
        PROXY_PASS = proxy[3] # password

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        chrome_options.add_extension(pluginfile)

        print("\nNow proxy: ", select_proxy, "\n")


    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
    chrome_options.add_argument('--no-sandbox')
    # options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("disable-infobars")
    
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
    return driver


class Person:
    def __init__(self) -> None:
        self.first_name = ri.get_first_name()
        self.last_name = ri.get_last_name()
        self.birthdate = ri.get_birthdate()

person1 = Person()

f= open('settings.txt', 'r')
settings = f.read()
split_settings = settings.splitlines()

provided_password = split_settings[0]
no_of_emails = int(split_settings[1])

    
def create_account(count):
  
    email = ri.get_email(person1)

    browser = changeproxy()
    # browser.maximize_window()
    browser.get('http://reddit.com/account/register/')
    time.sleep(randint(1,2))
    browser.find_element(By.ID, 'regEmail').click()
    browser.find_element(By.ID, 'regEmail').send_keys(email)
    browser.find_element(By.CSS_SELECTOR, 'button.AnimatedForm__submitButton:nth-child(1)').click() 
    
    time.sleep(3)
    browser.implicitly_wait(5)
    browser.find_element(By.CSS_SELECTOR, 'a.Onboarding__usernameSuggestion:nth-child(1)').click() 
    username = browser.find_element(By.CSS_SELECTOR, 'a.Onboarding__usernameSuggestion:nth-child(1)').text

    time.sleep(randint(1,2))
    browser.find_element(By.ID, 'regPassword').click()
    browser.find_element(By.ID, 'regPassword').send_keys(str(provided_password))

    browser.find_element(By.CSS_SELECTOR, 'button.AnimatedForm__submitButton:nth-child(3)' ).click() #clicks signup to show captcha

    print("Solving Captcha...")
    time.sleep(5)
    try: 
        solveCaptcha_pro(browser)
        sleep(1)
        browser.switch_to.default_content()
        time.sleep(2)
    except Exception as e:
        pass  
   
    try:
        browser.find_element(By.CSS_SELECTOR, 'button.AnimatedForm__submitButton:nth-child(3)' ).click()
        sleep(6)
        if "Dive into anything" in str(browser.title):
            with open('created_accounts.txt','a') as file:
                file.write(str(username)+ '\n')
                file.close()

                print("\n\nAccount#",count,": ",username, "created successfully")
                count +=1
                sleep(3)
        else:
            print("Account is not created successfully.")
        
    except Exception as err:
        print("err: ",err)

    return count
    

count = 1
while(count <= no_of_emails):
    count = create_account(count)
    
print("\n\n",no_of_emails," accounts created successfully!")


