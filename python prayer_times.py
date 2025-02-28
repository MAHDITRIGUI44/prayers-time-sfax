import time
import tkinter as tk
from datetime import datetime
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

# 🔹 إعداد WebDriver لـ Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # تشغيل بدون واجهة رسومية
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# 🔹 تشغيل متصفح Chrome باستخدام WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get(URL)

# 🔹 انتظار تحميل الصفحة بالكامل
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "GovList")))

# ✅ **1. اختيار ولاية صفاقس (`ID=27`)**
gov_list = Select(driver.find_element(By.ID, "GovList"))
gov_list.select_by_value("27")  # اختيار صفاقس
time.sleep(3)  # انتظار تحديث المواقيت بعد الطلب AJAX

# ✅ **2. انتظار تحميل المواقيت الجديدة**
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "T_fajr")))

# 🔹 استخراج HTML بعد تحديث الصفحة
html_source = driver.page_source
driver.quit()  # إغلاق المتصفح

# 🔹 تحليل الصفحة باستخدام BeautifulSoup
soup = BeautifulSoup(html_source, 'html.parser')

# ✅ **3. استخراج التقويم الهجري بشكل أكثر دقة**
def fetch_hijri_date():
    try:
        # البحث عن جميع عناصر <h5> والتحقق من النص الذي يحتوي على "التقويم الهجري"
        h5_elements = soup.find_all("h5")
        for h5 in h5_elements:
            if "التقويم الهجري" in h5.text:
                hijri_date = h5.find("span").text.strip()
                return hijri_date
        return "⚠️ لم يتم العثور على التقويم الهجري"
    except AttributeError:
        return "⚠️ خطأ أثناء جلب التقويم الهجري"

# ✅ **4. استخراج المواقيت الصحيحة**
def fetch_prayer_times():
    try:
        prayer_times = {
            "الصبح": soup.find("div", id="T_fajr").text.strip(),
            "الظهر": soup.find("div", id="T_Dohr").text.strip(),
            "العصر": soup.find("div", id="T_Asr").text.strip(),
            "المغرب": soup.find("div", id="T_Maghrib").text.strip(),
            "العشاء": soup.find("div", id="T_Isha").text.strip()
        }
        return prayer_times
    except AttributeError:
        print("⚠️ لم يتم العثور على مواقيت الصلاة!")
        return None

# ✅ **5. تحديث واجهة التطبيق بالمواقيت الصحيحة**
def update_prayer_times():
    prayer_times = fetch_prayer_times()
    if prayer_times:
        for prayer, time in prayer_times.items():
            if prayer in prayer_labels:
                prayer_labels[prayer].config(text=f"{prayer}: {time}")
        error_label.config(text="✅ تم تحديث المواقيت بنجاح!")
    else:
        error_label.config(text="⚠️ تعذر جلب مواقيت الصلاة.")

# ✅ **6. إنشاء واجهة التطبيق باستخدام Tkinter**
root = tk.Tk()
root.title("🕌 مواقيت الصلاة - صفاقس")
root.geometry("350x400")  # زيادة الارتفاع قليلاً لاستيعاب التقويم الهجري
root.configure(bg="#f8f9fa")

# ✅ **7. عرض التقويم الهجري في الأعلى**
hijri_date = fetch_hijri_date()
hijri_label = tk.Label(root, text=f"📅 التقويم الهجري: {hijri_date}", font=("Arial", 12, "bold"), fg="#349667", bg="#f8f9fa")
hijri_label.pack(pady=5)

# 🔹 عنوان التطبيق
title_label = tk.Label(root, text="🕌 مواقيت الصلاة - صفاقس", font=("Arial", 14, "bold"), bg="#f8f9fa", fg="#007bff")
title_label.pack(pady=10)

# 🔹 تاريخ اليوم الميلادي
today = datetime.today().strftime("%d/%m/%Y")
date_label = tk.Label(root, text=f"📅 {today}", font=("Arial", 12), bg="#f8f9fa", fg="#6c757d")
date_label.pack()

# 🔹 إطار لعرض المواقيت
frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
frame.pack(pady=10, padx=10, fill="both", expand=True)

# 🔹 إنشاء القيم الافتراضية لعرض المواقيت
prayer_labels = {
    "الصبح": tk.Label(frame, text="الصبح: --:--", font=("Arial", 12), bg="white"),
    "الظهر": tk.Label(frame, text="الظهر: --:--", font=("Arial", 12), bg="white"),
    "العصر": tk.Label(frame, text="العصر: --:--", font=("Arial", 12), bg="white"),
    "المغرب": tk.Label(frame, text="المغرب: --:--", font=("Arial", 12), bg="white"),
    "العشاء": tk.Label(frame, text="العشاء: --:--", font=("Arial", 12), bg="white")
}

for label in prayer_labels.values():
    label.pack(pady=5)

# 🔹 رسالة خطأ في حالة فشل جلب البيانات
error_label = tk.Label(root, text="", font=("Arial", 10), fg="red", bg="#f8f9fa")
error_label.pack()

# 🔹 جلب المواقيت وتحديث الواجهة عند تشغيل التطبيق
update_prayer_times()

# 🔹 تشغيل التطبيق
root.mainloop()
