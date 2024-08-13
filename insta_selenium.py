import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

try:
    username_input = driver.find_element(By.NAME, 'username')
    username = os.getenv('INSTAGRAM_USERNAME')
    username_input.send_keys(username)
    
    password_input = driver.find_element(By.NAME, 'password')
    password = os.getenv('INSTAGRAM_PASSWORD')
    password_input.send_keys(password)

    login_button = driver.find_element(By.CSS_SELECTOR, 'button._acan._acap._acas._aj1-._ap30')
    login_button.click()
    
    time.sleep(20) 
    
    save_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and contains(text(), "Not now")]'))
    )
    save_button.click()
    
    not_now_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._a9--._ap36._a9_1'))
    )
    not_now_button.click()
    
    articles = driver.find_elements(By.TAG_NAME, 'article')
    
    for i, article in enumerate(articles[:1]):
        print(article.text)
        
        post_image_element = article.find_elements(By.TAG_NAME, 'img')
        if len(post_image_element) > 1:
            image_element = post_image_element[1]
            image_url = image_element.get_attribute('src')
            print("Image URL:", image_url)
        else:
            video_element = driver.find_element(By.TAG_NAME, 'video')
            video_url = video_element.get_attribute('src')
            print(f"Video URL: {video_url}")
            
            
        if "Liked by" in article.text:
            parts = article.text.split('Liked by')
            if len(parts) > 1:
                likes_part = parts[1].split('\n')[0].strip()
                print("Likes:", likes_part)
            
            
        captions = driver.find_elements(By.CSS_SELECTOR, 'article div span.x1lliihq')
        for caption in captions:
            print('Caption: ', caption.text)
                   
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        username_element = driver.find_element(By.CSS_SELECTOR, 'span._ap3a')
        username = username_element.text 
        profile = f'{url}{username}/'
        driver.get(profile)
        
        try:
            list_items = driver.find_elements(By.XPATH, '//ul/li')
            print(f'Followers of {username}: ', list_items[1].text)

        except Exception as e:
            print("Error:", e)
        
        finally:
            driver.quit()
        
except Exception as e:
    print("Error:", e)
              
finally:
    driver.quit()