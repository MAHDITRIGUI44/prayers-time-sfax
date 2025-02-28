import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 🔹 رابط الموقع لجلب مواقيت الصلاة
URL = "https://www.affaires-religieuses.tn/public/ar"

# ✅ **إعداد WebDriver**
def init_driver():
    """
    Initializes and returns the Selenium WebDriver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # تشغيل بدون واجهة رسومية
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "GovList")))

    # اختيار ولاية صفاقس
    gov_list = Select(driver.find_element(By.ID, "GovList"))
    gov_list.select_by_value("27")  # اختيار صفاقس
    time.sleep(3)  # انتظار تحديث المواقيت

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "T_fajr")))
    return driver

# ✅ **استخراج بيانات الصفحة**
def get_page_soup(driver):
    """
    Extracts and returns the parsed HTML page source.
    """
    return BeautifulSoup(driver.page_source, 'html.parser')

# ✅ **جلب التقويم الهجري**
def fetch_hijri_date():
    """
    Fetches the Hijri date from the website.
    """
    try:
        driver = init_driver()
        soup = get_page_soup(driver)
        driver.quit()

        h5_elements = soup.find_all("h5")
        for h5 in h5_elements:
            if "التقويم الهجري" in h5.text:
                return h5.find("span").text.strip()
        return "⚠️ لم يتم العثور على التقويم الهجري"
    except AttributeError:
        return "⚠️ خطأ أثناء جلب التقويم الهجري"

# ✅ **جلب مواقيت الصلاة**
def fetch_prayer_times():
    """
    Fetches prayer times for Sfax from the website.
    """
    try:
        driver = init_driver()
        soup = get_page_soup(driver)
        driver.quit()

        return {
            "الصبح": soup.find("div", id="T_fajr").text.strip(),
            "الظهر": soup.find("div", id="T_Dohr").text.strip(),
            "العصر": soup.find("div", id="T_Asr").text.strip(),
            "المغرب": soup.find("div", id="T_Maghrib").text.strip(),
            "العشاء": soup.find("div", id="T_Isha").text.strip()
        }
    except AttributeError:
        return None
