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
        return None

# ✅ **5. تحديث واجهة التطبيق بالمواقيت الصحيحة**
def update_prayer_times():
    prayer_times = fetch_prayer_times()
    if prayer_times:
        for prayer, time in prayer_times.items():
            if prayer in prayer_labels:
                prayer_labels[prayer].config(text=f"{prayer}: {time}")
        error_label.config(text="✅ تم تحديث المواقيت بنجاح!", fg="green")
    else:
        error_label.config(text="⚠️ تعذر جلب مواقيت الصلاة.", fg="red")

# ✅ **6. إنشاء واجهة التطبيق باستخدام Tkinter**
root = tk.Tk()
root.title("🕌 مواقيت الصلاة - صفاقس")
root.configure(bg="#f8f9fa")

# ✅ **جعل النافذة تأخذ كامل الشاشة**
root.state("zoomed")    # Fullscreen mode

# ✅ **إضافة زر للخروج من وضع Fullscreen**
def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)  # Disable fullscreen

root.bind("<Escape>", exit_fullscreen)  # اضغط "Esc" للخروج من وضع Fullscreen

# ✅ **تنظيم الواجهة باستخدام grid()**
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# ✅ **7. عرض التقويم الهجري في الأعلى**
hijri_date = fetch_hijri_date()
hijri_label = tk.Label(root, text=f"📅 التقويم الهجري: {hijri_date}", font=("Arial", 18, "bold"), fg="#349667", bg="#f8f9fa")
hijri_label.grid(row=0, column=0, pady=10, sticky="ew")

# 🔹 عنوان التطبيق
title_label = tk.Label(root, text="🕌 مواقيت الصلاة - صفاقس", font=("Arial", 20, "bold"), bg="#f8f9fa", fg="#007bff")
title_label.grid(row=1, column=0, pady=10, sticky="ew")

# 🔹 تاريخ اليوم الميلادي
today = datetime.today().strftime("%d/%m/%Y")
date_label = tk.Label(root, text=f"📅 {today}", font=("Arial", 18), bg="#f8f9fa", fg="#6c757d")
date_label.grid(row=2, column=0, sticky="ew")

# 🔹 إطار لعرض المواقيت
frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
frame.grid(row=3, column=0, pady=20, padx=20, sticky="nsew")

# 🔹 السماح للإطار بالتمدد ديناميكياً
root.rowconfigure(3, weight=1)

# 🔹 إنشاء القيم الافتراضية لعرض المواقيت
prayer_labels = {}
prayers = ["الصبح", "الظهر", "العصر", "المغرب", "العشاء"]

for i, prayer in enumerate(prayers):
    prayer_labels[prayer] = tk.Label(frame, text=f"{prayer}: --:--", font=("Arial", 20), bg="white")
    prayer_labels[prayer].grid(row=i, column=0, pady=10, padx=20, sticky="ew")
    frame.rowconfigure(i, weight=1)

# 🔹 رسالة خطأ في حالة فشل جلب البيانات
error_label = tk.Label(root, text="", font=("Arial", 16), fg="red", bg="#f8f9fa")
error_label.grid(row=4, column=0, sticky="ew", pady=10)

# 🔹 جلب المواقيت وتحديث الواجهة عند تشغيل التطبيق
update_prayer_times()

# ✅ **تحديث ديناميكي عند تغيير حجم النافذة**
def on_resize(event):
    new_width = event.width
    new_height = event.height
    print(f"Resized: {new_width}x{new_height}")  # Debugging

root.bind("<Configure>", on_resize)

# 🔹 تشغيل التطبيق
root.mainloop()
