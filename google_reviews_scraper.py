from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrape_google_reviews(place_url, max_reviews=50):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(place_url)
    time.sleep(5)

    for _ in range(5):
        try:
            scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="User reviews"]')
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(2)
        except Exception as e:
            print("Scrolling error:", e)
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    reviews = []
    review_blocks = soup.select('div.jftiEf')
    for block in review_blocks[:max_reviews]:
        try:
            name = block.select_one('div.d4r55').text.strip()
            date = block.select_one('span.rsqaWe').text.strip()
            text = block.select_one('span.wiI7pd').text.strip()
            stars_element = block.select_one('span.Kk7lMc')
            stars = stars_element['aria-label'] if stars_element else ""

            reviews.append({
                "name": name,
                "date": date,
                "text": text,
                "rating": stars
            })
        except:
            continue

    return reviews
