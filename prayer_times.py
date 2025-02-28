import tkinter as tk
from datetime import datetime
from data import fetch_hijri_date, fetch_prayer_times

# ✅ **تحديث شاشة الصلاة**
def update_prayer_times(prayer_labels, error_label):
    """
    Updates the prayer times on the UI.
    """
    prayer_times = fetch_prayer_times()
    if prayer_times:
        for prayer, time in prayer_times.items():
            prayer_labels[prayer].config(text=f"{prayer}: {time}")
        error_label.config(text="✅ تم تحديث المواقيت بنجاح!", fg="green")
    else:
        error_label.config(text="⚠️ تعذر جلب مواقيت الصلاة.", fg="red")

# ✅ **عرض شاشة مواقيت الصلاة**
def show_prayer_times_screen(root, show_screen):
    """
    Creates and displays the prayer times screen.
    
    Parameters:
    - root: The main Tkinter window.
    - show_screen: Function to switch between screens.
    """
    prayer_screen = tk.Frame(root, bg="#f8f9fa")
    prayer_screen.grid(row=0, column=0, sticky="nsew")

    # عنوان الشاشة
    tk.Label(prayer_screen, text="🕌 مواقيت الصلاة - صفاقس", font=("Arial", 20, "bold"), bg="#f8f9fa", fg="#007bff").pack(pady=10)
    
    # التقويم الهجري
    hijri_date = fetch_hijri_date()
    tk.Label(prayer_screen, text=f"📅 التقويم الهجري: {hijri_date}", font=("Arial", 16, "bold"), fg="#349667", bg="#f8f9fa").pack(pady=5)

    # تاريخ اليوم الميلادي
    today = datetime.today().strftime("%d/%m/%Y")
    tk.Label(prayer_screen, text=f"📅 {today}", font=("Arial", 16), bg="#f8f9fa", fg="#6c757d").pack()

    # إطار عرض المواقيت
    frame = tk.Frame(prayer_screen, bg="white", bd=2, relief="ridge")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # إنشاء القيم الافتراضية لعرض المواقيت
    prayer_labels = {}
    prayers = ["الصبح", "الظهر", "العصر", "المغرب", "العشاء"]

    for prayer in prayers:
        prayer_labels[prayer] = tk.Label(frame, text=f"{prayer}: --:--", font=("Arial", 18), bg="white")
        prayer_labels[prayer].pack(pady=5)

    # رسالة الخطأ
    error_label = tk.Label(prayer_screen, text="", font=("Arial", 14), fg="red", bg="#f8f9fa")
    error_label.pack()

    # زر العودة
    tk.Button(prayer_screen, text="⬅ العودة", font=("Arial", 14), command=lambda: show_screen("home")).pack(pady=10)

    # تحديث المواقيت عند فتح الشاشة
    update_prayer_times(prayer_labels, error_label)

    return prayer_screen
