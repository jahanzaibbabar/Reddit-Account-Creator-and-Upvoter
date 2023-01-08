from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


# def solveCaptcha_pro(driver):
#     driver.implicitly_wait(10)

#     g_recaptcha = driver.find_elements(By.ID, 'g-recaptcha')[0]
#     outerIframe = g_recaptcha.find_element(By.TAG_NAME, 'iframe')
#     outerIframe.click()

#     try:
#         iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        
#         for index in range(len(iframes)):
#             driver.switch_to.default_content()
#             iframe = driver.find_elements(By.TAG_NAME, 'iframe')[index]
#             driver.switch_to.frame(iframe)

#             try:
#                 driver.implicitly_wait(2)
#                 db = driver.find_element(By.CLASS_NAME, "help-button-holder")
#                 db.click()
#                 print("Captcha Solved")
            
#             except Exception as e:
#                 pass

#     except Exception as e:
#                pass

#     print("done")
#     sleep(537844)



def solveCaptcha_pro(driver):
    while True:
        try:
            sleep(5)
            driver.implicitly_wait(4)
            g_recaptcha = driver.find_elements(By.ID, 'g-recaptcha')[0]
            # g_recaptcha = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'g-recaptcha')[0]))
            driver.implicitly_wait(4)
            # outerIframe = WebDriverWait(g_recaptcha, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe')))
            outerIframe = g_recaptcha.find_element(By.TAG_NAME, 'iframe')
            outerIframe.click()
            print("clicked")
        except Exception as err:
            print("waiting to load captcha", err)

        try:
            driver.implicitly_wait(5)
            iframe = driver.find_element(By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']")
            driver.switch_to.frame(iframe)
            break
        except Exception as err:
            print(err)

    sleep(1)
    while True:
        try:
            driver.implicitly_wait(2)
            # driver.switch_to.frame(iframes)
            # db = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[4]//button')
            db = driver.find_element(By.CLASS_NAME, "help-button-holder")
            db.click()
            sleep(5)
            try:
                driver.implicitly_wait(0.1)
                reloadbtn = driver.find_element(By.ID, "recaptcha-reload-button")
                reloadbtn.click()
            except:
                break
        except Exception as e:
            print('captcha solve btn not found')
            break

    print("Captcha Solved")

