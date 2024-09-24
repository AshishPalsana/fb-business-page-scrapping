import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


service = Service(chrome_driver_path="path_to_your_chromedriver")


driver = webdriver.Chrome(service=service, options=chrome_options)

wait = WebDriverWait(driver, 10)


def scrape_facebook_page(url):
    try:
        driver.get(url)
        time.sleep(5)

        # Initialize variables
        page_title, email, website, reviews, phone_number, address = (
            "",
            "",
            "",
            "",
            "",
            "",
        )
        followers_text, likes_text, href = "", "", ""

        try:
            element_to_click = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div",
                    )
                )
            )
            element_to_click.click()
            print("Clicked on the specified element.")
        except Exception as e:
            print(f"An error occurred while clicking: {e}")
            return None

        # Scrape page title
        try:
            h1_element = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "h1.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1vvkbs.x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz",
                    )
                )
            )
            page_title = h1_element.text
        except TimeoutException:
            page_title = ""

        # Scrape email
        try:
            email_element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[contains(text(), '@')]")
                )
            )
            email = email_element.text
        except TimeoutException:
            email = ""

        # Scrape website
        try:
            website_element = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//span[contains(text(), '.com') and not(contains(text(), '@'))]",
                    )
                )
            )
            website = website_element.text
        except TimeoutException:
            website = ""

        # Scrape reviews
        try:
            reviews_element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[contains(text(), 'reviews')]")
                )
            )
            reviews = reviews_element.text
        except TimeoutException:
            reviews = ""

        # Scrape followers
        try:
            followers_element = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a[2]",
            )
            followers_text = followers_element.text
        except Exception as e:
            print(f"An error occurred while locating followers: {e}")
            followers_text = ""

        # Scrape likes
        try:
            likes_element = driver.find_element(
                By.CSS_SELECTOR,
                "a.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1sur9pj.xkrqix3.xi81zsa.x1s688f",
            )
            likes_text = likes_element.text
        except Exception as e:
            print(f"An error occurred while locating likes: {e}")
            likes_text = ""

        # Scrape phone number
        try:
            phone_element = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//span[contains(text(), '+') and not(contains(text(), '@'))]",
                    )
                )
            )
            phone_number = phone_element.text
        except TimeoutException:
            phone_number = ""

        # Scrape profile image URL
        try:
            profile_image_element = wait.until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div.x15sbx0n.x1xy773u.x390vds.xb2vh1x.x14xzxk9.x18u1y24.xs6kywh.x5wy4b0 div.x1rg5ohu.x1n2onr6.x3ajldb.x1ja2u2z svg image",
                    )
                )
            )
            href = profile_image_element.get_attribute("xlink:href")
        except TimeoutException:
            href = "Element not found or page took too long to load."

        # Scrape Address
        try:
            div_elements = wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        "div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.x1nhvcw1.x1qjc9v5.xozqiw3.x1q0g3np.xyamay9.xykv574.xbmpl8g.x4cne27.xifccgj",
                    )
                )
            )
            for element in div_elements:
                address_text = element.text
                if address_text.count(",") >= 2:
                    address = address_text
                    break
        except Exception as e:
            print(f"An error occurred while locating address: {e}")
            address = "Address not found"

        # Scrape posts
        post_counter = 0
        seen_posts = set()
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z",
                        )
                    )
                )

                posts = driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z",
                )
                new_posts = 0

                for post in posts:
                    post_id = post.text
                    if post_id not in seen_posts:
                        seen_posts.add(post_id)
                        post_counter += 1
                        new_posts += 1

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            except Exception as e:
                print(f"An error occurred while scraping: {e}")
                break

        # Print results
        print(f"Page Title: {page_title}")
        print(f"Followers: {followers_text}")
        print(f"Likes: {likes_text}")
        print(f"Email: {email}")
        print(f"Contact Number: {phone_number}")
        print(f"Website: {website}")
        print(f"Reviews: {reviews}")
        print(f"Profile Image URL: {href}")
        print(f"Address: {address}")
        print(f"Total number of posts scraped: {post_counter}")

        return {
            "Page Title": page_title,
            "Followers": followers_text,
            "Likes": likes_text,
            "Email": email,
            "Phone Number": phone_number,
            "Website": website,
            "Reviews": reviews,
            "Profile Image URL": href,
            "Address": address,
            "Total Number of Posts Scraped": post_counter,
        }

    except TimeoutException:
        print("Timeout occurred while trying to find elements.")
        return None


# Read URLs from 'url.xlsx'
urls_df = pd.read_excel("url.xlsx")
urls = urls_df["URL"].tolist()

results = []

for url in urls:
    print(f"Scraping URL: {url}")
    data = scrape_facebook_page(url)
    if data:
        results.append(data)

# Save results to 'facebook_page_data.xlsx'
results_df = pd.DataFrame(results)
results_df.to_excel("facebook_page_data.xlsx", index=False)
print("Data has been saved to facebook_page_data.xlsx")


driver.quit()
