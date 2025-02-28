import tkinter as tk

def show_second_screen(root, show_screen):
    """
    This function creates and displays the second (extra) screen.
    
    Parameters:
    - root: The main Tkinter window.
    - show_screen: Function to switch between screens.
    """
    # Create the extra screen frame
    extra_screen = tk.Frame(root, bg="#f8f9fa")
    extra_screen.grid(row=0, column=0, sticky="nsew")

    # Title Label
    tk.Label(extra_screen, text="📖 شاشة إضافية", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=20)

    # Return Button to go back to the Main Menu
    tk.Button(extra_screen, text="⬅ العودة", font=("Arial", 14), command=lambda: show_screen("home")).pack(pady=10)

    return extra_screen
