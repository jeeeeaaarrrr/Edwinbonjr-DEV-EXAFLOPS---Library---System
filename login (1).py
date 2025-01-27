import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3


# Custom style for buttons with rounded corners
class RoundButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(relief="flat", borderwidth=0)


# Database setup
def setup_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"""
    )
    conn.commit()
    conn.close()


# Function to toggle password visibility
def toggle_password_visibility(entry, var, check):
    if var.get():
        entry.config(show="")
        check.config(selectcolor="blue")  # Change to blue when checked
    else:
        entry.config(show="*")
        check.config(selectcolor="white")  # Reset back to white when unchecked


# User login for general users
def login_user():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        if c.fetchone():
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")
        conn.close()
    else:
        messagebox.showerror("Error", "Please enter both username and password.")


def on_login_student():
    # Hide all existing widgets and show student login form
    for widget in root.winfo_children():
        widget.place_forget()
    login_frame.pack(fill="both", expand=True)
    login_frame.lift()


def on_login_admin():
    # Hide all existing widgets and show admin login form
    for widget in root.winfo_children():
        widget.place_forget()
    admin_login_frame.pack(fill="both", expand=True)
    admin_login_frame.lift()


def admin_login():
    username = admin_username_entry.get()
    password = admin_password_entry.get()

    if username and password:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        if c.fetchone():
            messagebox.showinfo("Success", "Admin Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")
        conn.close()
    else:
        messagebox.showerror("Error", "Please enter both username and password.")


def on_sign_up():
    # Hide all existing widgets and show sign up form
    for widget in root.winfo_children():
        widget.place_forget()

    # Create a new frame for sign-up
    sign_up_frame = tk.Frame(root, bg="maroon")
    sign_up_frame.pack(fill="both", expand=True)
    sign_up_frame.lift()

    # Add UI elements for sign-up
    username_label = tk.Label(
        sign_up_frame,
        text="Enter PUP ID:",
        bg="maroon",
        fg="white",
        font=("Helvetica", 14, "bold"),
    )
    username_label.pack(pady=10)

    username_entry = tk.Entry(
        sign_up_frame, borderwidth=5, width=30, font=("Helvetica", 12)
    )
    username_entry.pack(pady=10)

    password_label = tk.Label(
        sign_up_frame,
        text="Create Password:",
        bg="maroon",
        fg="white",
        font=("Helvetica", 14, "bold"),
    )
    password_label.pack(pady=10)

    password_entry = tk.Entry(
        sign_up_frame, borderwidth=5, show="*", width=30, font=("Helvetica", 12)
    )
    password_entry.pack(pady=10)

    show_password_var = tk.BooleanVar()
    show_password_check = tk.Checkbutton(
        sign_up_frame,
        text="Show Password",
        variable=show_password_var,
        command=lambda: toggle_password_visibility(
            password_entry, show_password_var, show_password_check
        ),
        bg="maroon",
        fg="white",
        selectcolor="white",  # Start with white
        activebackground="darkred",
        indicatoron=1,
        height=1,
        width=15,  # Increased width for better visibility
    )
    show_password_check.pack(pady=5, anchor="c")

    reenterpassword_label = tk.Label(
        sign_up_frame,
        text="Re-enter Password:",
        bg="maroon",
        fg="white",
        font=("Helvetica", 14, "bold"),
    )
    reenterpassword_label.pack(pady=10)

    reenterpassword_entry = tk.Entry(
        sign_up_frame, borderwidth=5, show="*", width=30, font=("Helvetica", 12)
    )
    reenterpassword_entry.pack(pady=10)

    reenter_show_password_var = tk.BooleanVar()
    reenter_show_password_check = tk.Checkbutton(
        sign_up_frame,
        text="Show Password",
        variable=reenter_show_password_var,
        command=lambda: toggle_password_visibility(
            reenterpassword_entry,
            reenter_show_password_var,
            reenter_show_password_check,
        ),
        bg="maroon",
        fg="white",
        selectcolor="white",  # Start with white
        activebackground="darkred",
        indicatoron=1,
        height=1,
        width=15,  # Increased width for better visibility
    )
    reenter_show_password_check.pack(pady=5, anchor="c")

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        reenter_password = reenterpassword_entry.get()

        if username and password and reenter_password:
            if password == reenter_password:
                conn = sqlite3.connect("users.db")
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username = ?", (username,))
                if c.fetchone() is None:
                    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
                    conn.commit()
                    messagebox.showinfo("Success", "Registration successful!")
                    go_back()  # Return to the main interface after successful registration
                else:
                    messagebox.showerror("Error", "Username already exists!")
                conn.close()
            else:
                messagebox.showerror("Error", "Passwords do not match!")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    signup_button = tk.Button(
        sign_up_frame,
        text="Signup",
        command=register_user,
        bg="#FFD700",
        fg="maroon",
        font=("Helvetica", 12),
        width=10,
        height=1,
    )
    signup_button.pack(pady=10)

    back_button = tk.Button(
        sign_up_frame,
        text="Back",
        command=go_back,
        bg="white",
        fg="maroon",
        font=("Helvetica", 12),
        width=10,
        height=1,
    )
    back_button.pack(pady=10)


def go_back():
    # Hide login frame, admin login frame, and sign up frame, then show original interface
    for widget in root.winfo_children():
        widget.pack_forget()
    setup_initial_interface()


def setup_initial_interface():
    # Resetting the initial interface
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    header_frame.pack(fill="x")
    login_student_button.place(relx=0.5, y=440, anchor="center")
    login_admin_button.place(relx=0.5, y=495, anchor="center")
    sign_up_button.place(relx=0.5, y=550, anchor="center")


# Initialize the Tkinter app
root = tk.Tk()
root.title("Library System")
root.geometry("500x650")  # Increased window height

# Load background image
try:
    background_image = Image.open(r"Images\download.png")
    background_image = background_image.resize((1600, 1600), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
except FileNotFoundError:
    print("Error: Background image not found. Please check the file path.")
    background_photo = None

# Setting background image
background_label = tk.Label(root, image=background_photo)
if background_photo:
    background_label.image = background_photo
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add the red header background
header_frame = tk.Frame(root, bg="#800000", height=300)
header_frame.pack(fill="x")

# Add university logo
canvas = tk.Canvas(
    header_frame, width=100, height=100, bg="#800000", highlightthickness=0
)
canvas.pack(pady=20)

# Load and display image
try:
    logo_image = Image.open(r"Images\puplogo.png").resize((100, 100))
    logo = ImageTk.PhotoImage(logo_image)
    canvas.create_image(50, 50, image=logo)
    canvas.image = logo  # Prevent garbage collection
except FileNotFoundError:
    print("Error: Logo image not found. Please check the file path.")

# University and Library Text
university_name = tk.Label(
    header_frame,
    text="Polytechnic University of the Philippines",
    bg="#800000",
    fg="white",
    font=("Helvetica", 14),
)
university_name.pack()

library_label = tk.Label(
    header_frame,
    text="LIBRARY",
    bg="#800000",
    fg="white",
    font=("Helvetica", 24, "bold"),
)
library_label.pack(pady=15)

# Login Frame for general users
login_frame = tk.Frame(root, bg="maroon")

username_label = tk.Label(
    login_frame,
    text="PUP ID:",
    bg="maroon",
    fg="white",
    font=("Helvetica", 14, "bold"),
)
username_label.pack(pady=10)

username_entry = tk.Entry(login_frame, borderwidth=5, width=30, font=("Helvetica", 12))
username_entry.pack(pady=10)

password_label = tk.Label(
    login_frame,
    text="Password:",
    bg="maroon",
    fg="white",
    font=("Helvetica", 14, "bold"),
)
password_label.pack(pady=10)

password_entry = tk.Entry(
    login_frame, borderwidth=5, show="*", width=30, font=("Helvetica", 12)
)
password_entry.pack(pady=10)

show_password_var = tk.BooleanVar()
show_password_check = tk.Checkbutton(
    login_frame,
    text="Show Password",
    variable=show_password_var,
    command=lambda: toggle_password_visibility(
        password_entry, show_password_var, show_password_check
    ),
    bg="maroon",
    fg="white",
    selectcolor="white",  # Start with white
    activebackground="darkred",
    indicatoron=1,
    height=1,
    width=15,  # Increased width for better visibility
)
show_password_check.pack(pady=5, anchor="c")

login_button = tk.Button(
    login_frame,
    text="Login",
    command=login_user,
    bg="#FFD700",
    fg="maroon",
    font=("Helvetica", 12),
    width=10,
    height=1,
)
login_button.pack(pady=10)

back_button = tk.Button(
    login_frame,
    text="Back",
    command=go_back,
    bg="white",
    fg="maroon",
    font=("Helvetica", 12),
    width=10,
    height=1,
)
back_button.pack(pady=10)

# Admin Login Frame
admin_login_frame = tk.Frame(root, bg="maroon")

admin_username_label = tk.Label(
    admin_login_frame,
    text="Admin Username:",
    bg="maroon",
    fg="white",
    font=("Helvetica", 14, "bold"),
)
admin_username_label.pack(pady=10)

admin_username_entry = tk.Entry(
    admin_login_frame, borderwidth=5, width=30, font=("Helvetica", 12)
)
admin_username_entry.pack(pady=10)

admin_password_label = tk.Label(
    admin_login_frame,
    text="Admin Password:",
    bg="maroon",
    fg="white",
    font=("Helvetica", 14, "bold"),
)
admin_password_label.pack(pady=10)

admin_password_entry = tk.Entry(
    admin_login_frame, borderwidth=5, show="*", width=30, font=("Helvetica", 12)
)
admin_password_entry.pack(pady=10)

admin_show_password_var = tk.BooleanVar()
admin_show_password_check = tk.Checkbutton(
    admin_login_frame,
    text="Show Password",
    variable=admin_show_password_var,
    command=lambda: toggle_password_visibility(
        admin_password_entry, admin_show_password_var, admin_show_password_check
    ),
    bg="maroon",
    fg="white",
    selectcolor="white",  # Start with white
    activebackground="darkred",
    indicatoron=1,
    height=1,
    width=15,  # Increased width for better visibility
)
admin_show_password_check.pack(pady=5, anchor="c")

admin_login_button = tk.Button(
    admin_login_frame,
    text="Login",
    command=admin_login,
    bg="#FFD700",
    fg="maroon",
    font=("Helvetica", 12),
    width=10,
    height=1,
)
admin_login_button.pack(pady=10)

admin_back_button = tk.Button(
    admin_login_frame,
    text="Back",
    command=go_back,
    bg="white",
    fg="maroon",
    font=("Helvetica", 12),
    width=10,
    height=1,
)
admin_back_button.pack(pady=10)

# Buttons for Login and Register with adjusted size
login_student_button = RoundButton(
    root,
    text="LOG IN AS STUDENT",
    command=on_login_student,
    bg="#800000",
    fg="white",
    font=("Helvetica", 12),
    width=20,
    height=2,
)
login_student_button.place(relx=0.5, y=440, anchor="center")

login_admin_button = RoundButton(
    root,
    text="LOG IN AS ADMIN",
    command=on_login_admin,
    bg="#0000FF",
    fg="white",
    font=("Helvetica", 12),
    width=20,
    height=2,
)
login_admin_button.place(relx=0.5, y=495, anchor="center")

# New button for Sign Up with adjusted size
sign_up_button = RoundButton(
    root,
    text="SIGN UP YOUR PUP ID",
    command=on_sign_up,
    bg="#008000",
    fg="white",
    font=("Helvetica", 12),
    width=20,
    height=2,
)
sign_up_button.place(relx=0.5, y=550, anchor="center")

# Setup database
setup_database()

# Start the GUI loop
setup_initial_interface()
root.mainloop()
