import time
import os
import pyperclip
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()
options = Options()
options.headless = True

url = 'https://www.instagram.com/'

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
time.sleep(30)

try:
    username_input = driver.find_element(By.NAME, 'username')
    username = os.getenv('INSTAGRAM_USERNAME')
    username_input.send_keys('sajara6355')
    
    password_input = driver.find_element(By.NAME, 'password')
    password = os.getenv('INSTAGRAM_PASSWORD')
    password_input.send_keys('Riffat@1100')

    login_button = driver.find_element(By.CSS_SELECTOR, 'button._acan._acap._acas._aj1-._ap30')
    login_button.click()
    
    time.sleep(30) 
    
    save_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and contains(text(), "Not now")]'))
    )
    save_button.click()
    
    time.sleep(5) 
    
    not_now_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._a9--._ap36._a9_1'))
    )
    not_now_button.click()
    time.sleep(10) 
    
    articles = driver.find_elements(By.TAG_NAME, 'article')
    
    for i, article in enumerate(articles[:1]):
        post_image_element = article.find_elements(By.TAG_NAME, 'img')
        if len(post_image_element) > 1:
            image_element = post_image_element[1]
            image_url = image_element.get_attribute('src')
            print("Image URL:", image_url)
        else:
            time.sleep(10)
            svg_element = article.find_element(By.CSS_SELECTOR ,'svg.x1lliihq.x1n2onr6.x5n08af')
            svg_element.click()
            
            time.sleep(10)
            copy_link_button = WebDriverWait(article, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Copy link']"))
    )
            time.sleep(5)
            if copy_link_button:
                copy_link_button.click()
                
                time.sleep(5)
                copied_link = pyperclip.paste()
                print("Copied link:", copied_link)
            
        wait = WebDriverWait(article, 10)
        caption_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span._ap3a._aaco._aacu._aacx._aad7._aade')) 
        )
        
        time.sleep(10)    
        caption = caption_element.text
        print("Caption:", caption)
            
        time.sleep(10)
        if "Liked by" in article.text:
            parts = article.text.split('Liked by')
            if len(parts) > 1:
                likes_part = parts[1].split('\n')[0].strip()
                print("Likes:", likes_part)
                
            
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        username_element = article.find_element(By.CSS_SELECTOR, 'span._ap3a')
        username = username_element.text 
        profile = f'{url}{username}/'
        driver.get(profile)
        
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, '//ul/li')))

            list_items = driver.find_elements(By.XPATH, '//ul/li')
            print(f'Followers of {username}: ',list_items[1].text)

        except Exception as e:
            print("Error:", e)
        
        finally:
            driver.quit()
        
except Exception as e:
    print("Error:", e)
              
finally:
    driver.quit()
    
