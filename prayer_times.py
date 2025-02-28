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

# 🔹 تشغيل WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get(URL)

# 🔹 انتظار تحميل الصفحة
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "GovList")))

# ✅ اختيار ولاية صفاقس
gov_list = Select(driver.find_element(By.ID, "GovList"))
gov_list.select_by_value("27")
time.sleep(3)

# ✅ انتظار تحميل المواقيت
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "T_fajr")))

# 🔹 استخراج HTML
html_source = driver.page_source
driver.quit()

# 🔹 تحليل الصفحة باستخدام BeautifulSoup
soup = BeautifulSoup(html_source, 'html.parser')

# ✅ **جلب التقويم الهجري**
def fetch_hijri_date():
    try:
        h5_elements = soup.find_all("h5")
        for h5 in h5_elements:
            if "التقويم الهجري" in h5.text:
                return h5.find("span").text.strip()
        return "⚠️ لم يتم العثور على التقويم الهجري"
    except AttributeError:
        return "⚠️ خطأ أثناء جلب التقويم الهجري"

# ✅ **جلب مواقيت الصلاة**
def fetch_prayer_times():
    try:
        return {
            "الصبح": soup.find("div", id="T_fajr").text.strip(),
            "الظهر": soup.find("div", id="T_Dohr").text.strip(),
            "العصر": soup.find("div", id="T_Asr").text.strip(),
            "المغرب": soup.find("div", id="T_Maghrib").text.strip(),
            "العشاء": soup.find("div", id="T_Isha").text.strip()
        }
    except AttributeError:
        return None

# ✅ **تحديث شاشة الصلاة**
def update_prayer_times():
    prayer_times = fetch_prayer_times()
    if prayer_times:
        for prayer, time in prayer_times.items():
            prayer_labels[prayer].config(text=f"{prayer}: {time}")
        error_label.config(text="✅ تم تحديث المواقيت بنجاح!", fg="green")
    else:
        error_label.config(text="⚠️ تعذر جلب مواقيت الصلاة.", fg="red")

# ✅ **تبديل الشاشات**
def show_screen(screen):
    screen.tkraise()

# ✅ **إنشاء نافذة التطبيق**
root = tk.Tk()
root.title("🕌 مواقيت الصلاة - صفاقس")
root.state("zoomed")  # شاشة كاملة

# ✅ **زر الخروج من Full-Screen**
def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

# ✅ **إعداد الإطارات (3 شاشات)**
main_menu = tk.Frame(root, bg="#f8f9fa")
prayer_screen = tk.Frame(root, bg="#f8f9fa")
extra_screen = tk.Frame(root, bg="#f8f9fa")

for frame in (main_menu, prayer_screen, extra_screen):
    frame.grid(row=0, column=0, sticky="nsew")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# ✅ **تصميم الشاشة الرئيسية**
tk.Label(main_menu, text="📌 القائمة الرئيسية", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=20)
tk.Button(main_menu, text="🕌 مواقيت الصلاة", font=("Arial", 16), command=lambda: show_screen(prayer_screen)).pack(pady=10)
tk.Button(main_menu, text="📖 شاشة إضافية", font=("Arial", 16), command=lambda: show_screen(extra_screen)).pack(pady=10)

# ✅ **تصميم شاشة مواقيت الصلاة**
tk.Label(prayer_screen, text="🕌 مواقيت الصلاة - صفاقس", font=("Arial", 20, "bold"), bg="#f8f9fa", fg="#007bff").pack(pady=10)
tk.Label(prayer_screen, text=f"📅 التقويم الهجري: {fetch_hijri_date()}", font=("Arial", 16, "bold"), fg="#349667", bg="#f8f9fa").pack(pady=5)
tk.Label(prayer_screen, text=f"📅 {datetime.today().strftime('%d/%m/%Y')}", font=("Arial", 16), bg="#f8f9fa", fg="#6c757d").pack()

frame = tk.Frame(prayer_screen, bg="white", bd=2, relief="ridge")
frame.pack(pady=20, padx=20, fill="both", expand=True)

prayer_labels = {}
prayers = ["الصبح", "الظهر", "العصر", "المغرب", "العشاء"]

for prayer in prayers:
    prayer_labels[prayer] = tk.Label(frame, text=f"{prayer}: --:--", font=("Arial", 18), bg="white")
    prayer_labels[prayer].pack(pady=5)

error_label = tk.Label(prayer_screen, text="", font=("Arial", 14), fg="red", bg="#f8f9fa")
error_label.pack()

# ✅ **زر العودة**
tk.Button(prayer_screen, text="⬅ العودة", font=("Arial", 14), command=lambda: show_screen(main_menu)).pack(pady=10)

# ✅ **تصميم الشاشة الإضافية**
tk.Label(extra_screen, text="📖 شاشة إضافية", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=20)
tk.Button(extra_screen, text="⬅ العودة", font=("Arial", 14), command=lambda: show_screen(main_menu)).pack(pady=10)

# ✅ **تحديث المواقيت عند بدء التطبيق**
update_prayer_times()

# ✅ **إظهار شاشة مواقيت الصلاة عند بدء التشغيل**
show_screen(prayer_screen)  # 🔹 الآن تبدأ الشاشة على مواقيت الصلاة

# ✅ **تشغيل التطبيق**
root.mainloop()
