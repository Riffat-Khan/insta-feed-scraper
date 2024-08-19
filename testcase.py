import time
import os
import json
import pyperclip
import traceback
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
scraped_data = [] 

url = 'https://www.instagram.com/'

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)
time.sleep(10)

try:
    username_input = driver.find_element(By.NAME, 'username')
    username = os.getenv('INSTAGRAM_USERNAME')
    username_input.send_keys(username)
    
    password_input = driver.find_element(By.NAME, 'password')
    password = os.getenv('INSTAGRAM_PASSWORD')
    password_input.send_keys(password)

    login_button = driver.find_element(By.CSS_SELECTOR, 'button._acan._acap._acas._aj1-._ap30')
    login_button.click()
    time.sleep(10)
    
    pets_url = f'{url}{"explore/tags/pets/"}'
    driver.get(pets_url)
    
    time.sleep(10)

    try:
        pets_feed = driver.find_elements(By.CSS_SELECTOR, 'a.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz._a6hd')
        time.sleep(10)
        reel_urls = [pet.get_attribute('href') for pet in pets_feed[:20]]
        print(reel_urls)
        
        for reel in reel_urls:
            try:
                driver.get(reel)

                time.sleep(5)
                caption_element = driver.find_element(By.CSS_SELECTOR, 'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')
                time.sleep(5)
                lines = caption_element.text.splitlines()
                caption_content = lines[2:]
                caption = '\n'.join(caption_content)
                print('Caption: ',caption)
                
                time.sleep(5)
                likes_element = driver.find_element(By.CSS_SELECTOR, "div.x1xp8e9x.x13fuv20.x178xt8z.x9f619.x1yrsyyn.x1pi30zi.x10b6aqq.x1swvt13.xh8yej3")
                lines = likes_element.text.splitlines()
                likes_content = lines[0]
                print('Likes: ',likes_content)
                            
                time.sleep(5)
                svg_element = driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="More options"]')
                svg_element.click()

                copy_link_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Copy link']"))
                )
                time.sleep(5)
                if copy_link_button:
                    copy_link_button.click()
                    
                    time.sleep(5)
                    copied_link = pyperclip.paste()
                    print("Copied link:", copied_link)
                    
                    
                username_element =  driver.find_element(By.CSS_SELECTOR, 'span._ap3a._aaco._aacw._aacx._aad7._aade')
                username = username_element.text

                profile = f'{url}{username}/'
                driver.get(profile)
                time.sleep(10) 
                
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//ul/li'))
                    )
                    follower_element = driver.find_elements(By.XPATH, '//ul/li')
                    followers = follower_element[1].text
                    print(f'Followers of {username}: ', followers)
                
                except Exception as e:
                    print("Error:", e)
                    print("Traceback:", traceback.format_exc())
                    
                driver.back()
            except Exception as e:
                print("Error:", e)
                print("Traceback:", traceback.format_exc())
                
            data = {
                'caption': caption, 
                'likes': likes_content, 
                'link': copied_link, 
                'followers': followers,
            }
            scraped_data.append(data)

        with open('data.json', 'a') as f:
            json.dump(scraped_data, f, indent=4)
                        
    except Exception as e:
        print("Error:", e)
        print("Traceback:", traceback.format_exc())

except Exception as e:
        print("Error:", e)
        print("Traceback:", traceback.format_exc())
              
finally:
    driver.quit()