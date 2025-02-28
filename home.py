import tkinter as tk

def show_home_screen(root, show_screen):
    """
    This function creates and displays the main menu screen.

    Parameters:
    - root: The main Tkinter window.
    - show_screen: Function to switch between screens.
    """
    # Create the main menu frame
    home_screen = tk.Frame(root, bg="#f8f9fa")
    home_screen.grid(row=0, column=0, sticky="nsew")

    # Title Label
    tk.Label(home_screen, text="📌 القائمة الرئيسية", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=20)

    # Button to go to Prayer Times screen
    tk.Button(home_screen, text="🕌 مواقيت الصلاة", font=("Arial", 16), command=lambda: show_screen("prayer")).pack(pady=10)

    # Button to go to the Second Screen
    tk.Button(home_screen, text="📖 شاشة إضافية", font=("Arial", 16), command=lambda: show_screen("second")).pack(pady=10)

    return home_screen
