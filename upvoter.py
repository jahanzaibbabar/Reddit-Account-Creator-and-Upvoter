from selenium import webdriver
import time 
import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import zipfile
from random import randint
from selenium.webdriver.common.action_chains import ActionChains

loginFile = 'created_accounts.txt'

# usera = open('user_agents.txt', 'r')
# ua = usera.read()
# user_agents = ua.splitlines()

proxy_file = open('proxies.txt', 'r')
proxies = proxy_file.read()
proxies_list = proxies.splitlines()

use_p = open('use_proxy.txt', 'r')
is_proxy = use_p.read() 

def changeproxy():

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


    chrome_options = webdriver.ChromeOptions()
    pluginfile = 'proxy_auth_plugin.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    
    if is_proxy == 'True' or is_proxy == 'true':
        chrome_options.add_extension(pluginfile)
        print("\nNow proxy: ", select_proxy, "\n")

    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--mute-audio')

    # chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
    return driver


def upvote_post(username, postLink):
    browser = changeproxy()
    browser.maximize_window()

    browser.get("https://www.reddit.com/login/")
    sleep(1)

    browser.find_element(By.ID, 'loginUsername').click()
    browser.find_element(By.ID, 'loginUsername').send_keys(str(username))
    sleep(1)
    browser.find_element(By.ID, 'loginPassword').click()
    browser.find_element(By.ID, 'loginPassword').send_keys(password)

    time.sleep(2)
    try:
        # browser.set_page_load_timeout(10)
        browser.find_element(By.CSS_SELECTOR, 'button.AnimatedForm__submitButton:nth-child(1)').click()
    except TimeoutException:
        pass

    sleep(3)

    try:
        browser.get(postLink)
        time.sleep(3)
    except TimeoutException:
        try:
            browser.get(postLink)
        except:
            pass
        pass

    browser.implicitly_wait(10)

    try:
        yes = browser.find_elements(By.CLASS_NAME, "_2nelDm85zKKmuD94NequP0")[1]
        action = ActionChains(browser)
        action.click(on_element = yes)
        action.perform()

    except Exception as e:
        browser.refresh()
        try:
            browser.implicitly_wait(10)
            yes = browser.find_elements(By.CLASS_NAME, "_2nelDm85zKKmuD94NequP0")[1]

            action = ActionChains(browser)
            action.click(on_element = yes)
            action.perform()
        except Exception as err:
            pass

    sleep(2)
    browser.implicitly_wait(10)
    browser.find_element(By.CLASS_NAME, "voteButton").click()
    print("\nUpvote Successfully!")
    sleep(2)
    browser.close()




f = open(loginFile, 'r')
data = f.read()
f.close()

usernames = data.splitlines()
print("\nAll Accounts", usernames)

f2 = open('settings.txt', 'r')
data2 = f2.read()
f2.close()

password = data2.splitlines()[0]
print('\nAccount password: ',password)

f3 = open('link.txt', 'r')
postLink = f3.read()
f3.close()

for link in postLink.splitlines():
    if len(link) != 0:
        for user in usernames:
            try:
                if len(user) != 0:
                    upvote_post(user,link)
            except:
                pass

