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
            prayer_labels[prayer].config(text=time)
        error_label.config(text="✅ تم تحديث المواقيت بنجاح!", fg="green")
    else:
        error_label.config(text="⚠️ تعذر جلب مواقيت الصلاة.", fg="red")

# ✅ **عرض شاشة مواقيت الصلاة بتنسيق جدول مشابه للصورة**
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
    frame.pack(pady=20, padx=20)

    # 🔹 **تهيئة العناوين العلوية**
    tk.Label(frame, text="(التوقيت)", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=6, pady=5)
    tk.Label(frame, text="التاريخ الهجري: ....", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=1, columnspan=2)
    tk.Label(frame, text="التاريخ الميلادي: ....", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=3, columnspan=2)

    # 🔹 **تهيئة عناوين أوقات الصلاة**
    tk.Label(frame, text="الجمعة: ....", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=0)
    tk.Label(frame, text="الصبح", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=1)
    tk.Label(frame, text="الظهر", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=2)
    tk.Label(frame, text="العصر", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=3)
    tk.Label(frame, text="المغرب", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=4)
    tk.Label(frame, text="العشاء", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=5)

    # 🔹 **تهيئة صف الأذان**
    tk.Label(frame, text="الأذان", font=("Arial", 12, "bold"), bg="white").grid(row=3, column=0)

    # متغيرات تخزين أوقات الصلاة
    prayer_labels = {
        "الصبح": tk.Label(frame, text="--:--", font=("Arial", 12), bg="white"),
        "الظهر": tk.Label(frame, text="--:--", font=("Arial", 12), bg="white"),
        "العصر": tk.Label(frame, text="--:--", font=("Arial", 12), bg="white"),
        "المغرب": tk.Label(frame, text="--:--", font=("Arial", 12), bg="white"),
        "العشاء": tk.Label(frame, text="--:--", font=("Arial", 12), bg="white"),
    }

    # وضع الأوقات داخل الجدول
    col_index = 1
    for prayer, label in prayer_labels.items():
        label.grid(row=3, column=col_index)
        col_index += 1

    # 🔹 **تهيئة صف الإقامة**
    tk.Label(frame, text="الإقامة", font=("Arial", 12, "bold"), bg="white").grid(row=4, column=0)
    
    # (يمكنك إضافة قيم الإقامة هنا إذا لزم الأمر)

    # رسالة الخطأ
    error_label = tk.Label(prayer_screen, text="", font=("Arial", 14), fg="red", bg="#f8f9fa")
    error_label.pack()

    # زر العودة
    tk.Button(prayer_screen, text="⬅ العودة", font=("Arial", 14), command=lambda: show_screen("home")).pack(pady=10)

    # تحديث المواقيت عند فتح الشاشة
    update_prayer_times(prayer_labels, error_label)

    return prayer_screen
