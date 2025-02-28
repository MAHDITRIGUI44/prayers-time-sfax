import tkinter as tk
from home import show_home_screen
from prayer_times import show_prayer_times_screen
from second_screen import show_second_screen

def show_screen(screen_name):
    """
    Switches to the requested screen.

    Parameters:
    - screen_name: The key name of the screen to be displayed.
    """
    screens[screen_name].tkraise()

def exit_fullscreen(event=None):
    """ Exits fullscreen mode when the 'Esc' key is pressed. """
    root.attributes("-fullscreen", False)

# ✅ **Initialize Tkinter root window**
root = tk.Tk()
root.title("🕌 مواقيت الصلاة - صفاقس")
root.state("zoomed")  # Start in fullscreen mode

# ✅ **Bind Escape Key to Exit Fullscreen**
root.bind("<Escape>", exit_fullscreen)

# ✅ **Create a dictionary to hold all screens**
screens = {}

# ✅ **Configure the window layout**
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# ✅ **Load and add screens to the dictionary**
screens["home"] = show_home_screen(root, show_screen)
screens["prayer"] = show_prayer_times_screen(root, show_screen)
screens["second"] = show_second_screen(root, show_screen)

# ✅ **Show the Prayer Times screen by default**
show_screen("prayer")

# ✅ **Start the Tkinter event loop**
root.mainloop()
