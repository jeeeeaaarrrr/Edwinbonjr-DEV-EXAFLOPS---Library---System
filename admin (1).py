import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk


# Database setup
def setup_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)"""
    )
    conn.commit()
    conn.close()


# User registration
def register_user():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        if c.fetchone() is None:
            c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Username already exists!")
        conn.close()
    else:
        messagebox.showerror("Error", "Please enter both username and password.")


# User login
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


# Create main window
root = tk.Tk()
root.title("Admin")
root.configure(bg="maroon")

# Add university logo
canvas = tk.Canvas(root, width=100, height=100, bg="#800000", highlightthickness=0)
canvas.pack(pady=20)

# Load and display image
try:
    logo_image = Image.open(r"Images\puplogo.png").resize(
        (100, 100)
    )  # Resize for consistency
    logo = ImageTk.PhotoImage(logo_image)
    canvas.create_image(50, 50, image=logo)
    canvas.image = logo  # Prevent garbage collection
except FileNotFoundError:
    print("Error: Logo image not found. Please check the file path.")

    # University and Library Text
university_name = tk.Label(
    text="Polytechnic University of the Philippines",
    bg="#800000",
    fg="white",
    font=("Helvetica", 14),
)
university_name.pack()

library_label = tk.Label(
    text="LIBRARY",
    bg="#800000",
    fg="white",
    font=("Helvetica", 24, "bold"),
)
library_label.pack()

# UI elements
# Adjusting size for labels, entries, and button using place()
username_label = tk.Label(
    root, text="Username", bg="maroon", fg="white", width=10, height=5
)
username_label.place(x=730, y=290)

username_entry = tk.Entry(root, width=30)
username_entry.place(x=675, y=350)

password_label = tk.Label(root, text="Password", bg="maroon", fg="white", width=10)
password_label.place(x=730, y=380)

password_entry = tk.Entry(root, show="*", width=30)
password_entry.place(x=675, y=410)

login_button = tk.Button(
    root,
    text="Login",
    command=login_user,
    bg="#FFD700",
    fg="maroon",
    width=10,
    height=1,
)
login_button.place(x=730, y=440)

# Setup database
setup_database()

# Run the main loop
root.mainloop()
