import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dateutil.parser import parse as parse_datetime
import time
import json

def login_to_X(driver, username, password):
    driver.get("https://x.com/login")
    time.sleep(15)

    user_input = driver.find_element(By.NAME, "text")
    user_input.send_keys(username)
    user_input.send_keys(Keys.ENTER)
    time.sleep(10)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(10)
def scroll_down(driver, scroll_times=6, delay=4):
    for _ in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    time.sleep(6)

def scrape_cz_binance():
    options = uc.ChromeOptions()
    # options.add_argument('--headless')  # Tắt nếu cần debug
    driver = uc.Chrome(options=options)
    
    login_to_X(driver, "madarinfdre", "Phuonghuyt1k29")
    url = "https://x.com/cz_binance"
    driver.get(url)
    time.sleep(60)
    scroll_down(driver, scroll_times=6, delay=4)
    posts = []
    elements = driver.find_elements(By.XPATH, '//article')

    for post in elements:
        try:
            #content = post.text
            timestamp_element = post.find_element(By.XPATH, './/time')
            timestamp_str = timestamp_element.get_attribute("datetime")
            timestamp =parse_datetime(timestamp_str)
            tweet_url = timestamp_element.find_element(By.XPATH, './..').get_attribute("href")
            content = post.text.strip()
            posts.append({
                "content": content,
                "datetime": timestamp.isoformat(),
                "url": tweet_url
            })
        except Exception as e:
            continue
    
    posts = sorted(posts, key=lambda x: x["datetime"], reverse=True)
    posts = posts[:10]
    driver.quit()

    with open("cz_binance_posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)
    print("Đã lưu 10 bài viết mới nhất")

if __name__ == "__main__":
    scrape_cz_binance()
