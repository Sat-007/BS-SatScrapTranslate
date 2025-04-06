
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import os
import requests

#service = Service(ChromeDriverManager().install()) 
#driver = webdriver.Chrome(service=service)
#

def search_automation(driver):
    MAX_ARTICLES = 5
    os.makedirs("images", exist_ok=True)
    '''
    The first step is to open the el paris website, wait for the content to load, I have used maximize_window() to maximize the browser screen 
    '''
    driver.get('https://elpais.com/')
    
    try:
        driver.maximize_window()
    except:
        pass
    
    time.sleep(2)
    wait = WebDriverWait(driver, 2)
    time.sleep(2)
    
    '''
    second step Encountering Cookies, handled it using selector and click on the button
    '''

    try:
        
        cookie_accept_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#didomi-notice-agree-button")))
        cookie_accept_button.click()
        time.sleep(2)
    except Exception as e:
        pass

    '''
    Navigating to the Opinion sectio nof the website, first lets check opinion is present and then click on it to navigate to the next tab which is the opinion tab
    '''
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
    opinion_link = driver.find_element(By.LINK_TEXT, "Opinión")
    opinion_link.click()
    wait.until(EC.url_contains("/opinion"))
    time.sleep(2)

    '''
    Extracting the top 5 articles which are present here on the opinion tab
    '''
    top_5_articles =  driver.find_elements(By.XPATH, "//article//a[@href]") 
    top_5_article_links = []
    seen = set()

    '''
    using a set to keep track of the number of urls and if len() > 5 break from the loop and append < 4 urls only
    '''
    for article in top_5_articles:
        href = article.get_attribute("href")
        if href and "/opinion/" in href and "editoriales" not in href and href not in seen:
            seen.add(href)
            top_5_article_links.append(href)
        if len(seen) == MAX_ARTICLES:
            break

    #print(top_5_article_links)

    data = []

    for i, link in enumerate(top_5_article_links):
        driver.get(link)
        page_wait = WebDriverWait(driver, 10)

        try:  
            title_element = page_wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1"))
            )
            title = title_element.text.strip()
        except Exception:
            title = "No Title"
            

        try:
            page_wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class, 'a_c')]//p | //div[contains(@class, 'a_c-sum')]//p"
                ))
            )
            #first_paragraph = driver.find_element(By.XPATH, "(//div[contains(@class, 'a_c')]//p)[1]")
            #content = first_paragraph.text.strip()
            body_content = driver.find_elements(By.XPATH, "//div[contains(@class, 'a_c')]//p")
            summary_paragraphs = driver.find_elements(By.XPATH, "//div[contains(@class, 'a_c-sum')]//p")
            all_paragraphs = body_content + summary_paragraphs
            content = "\n".join(p.text.strip() for p in all_paragraphs if p.text.strip())
            cleaned_content = content.replace("\n", "")

        except Exception:
            cleaned_content = "No content"

        '''
        Checking if there are any images associated with the article if there are then we store them else we just continue
        '''
        try:
            image_element = driver.find_element(By.XPATH, "//*[@id='main-content']//img")
            image_url = image_element.get_attribute("src")
            '''
            Save the image into a folder earlier created as images and associating with proper article index for the
            '''
            if image_url:
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                filename = f"article_{i + 1}.jpg"
                image_path = os.path.join("images", filename)

                with open(image_path, "wb") as f:
                    f.write(image_response.content)

        except Exception:
            image_url = None
        
        if title != "No Title" and cleaned_content and cleaned_content != "No content":
            data.append({
                "id": len(data) + 1,
                "url": link,
                "title": title,
                "content": cleaned_content,
                "image": image_url
            })
        
        #print(data)

    return data   

    



