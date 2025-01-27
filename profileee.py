import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("500x400")
root.title("Home")


def hide_indicators():
    home_indicate.config(bg="#F0F0F0")
    mybooks_indicate.config(bg="#F0F0F0")
    leaderboards_indicate.config(bg="#F0F0F0")
    profile_indicate.config(bg="#F0F0F0")


def indicate(lb):
    hide_indicators()
    lb.config(bg="#158aff")


def show_profile():
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Profile Picture
    profile_image = Image.open("Images\\avatar1.png")  # Ensure the path is correct
    profile_image = profile_image.resize(
        (300, 300), Image.Resampling.LANCZOS
    )  # Reduced size for better fit
    profile_photo = ImageTk.PhotoImage(profile_image)

    # Place the profile picture directly in main_frame using place()
    profile_label = tk.Label(main_frame, image=profile_photo, bg="#008080")
    profile_label.image = profile_photo  # Keep reference
    profile_label.place(x=500, y=70)  # Adjust these coordinates for precise positioning

    # Name - placed closer below the profile image
    name_label = tk.Label(
        main_frame,
        text="Janrey Balabis",
        font=("Arial", 20, "bold"),  # Increased font size for emphasis
        fg="white",
        bg="#008080",
    )
    name_label.place(x=560, y=400)  # Adjust these coordinates for precise positioning

    # Add label for books read
    books_read_label = tk.Label(
        main_frame,
        text="▶0 Books Read◀",
        font=("Arial", 14),  # Font size adjusted for visibility
        fg="red",
        bg="#008080",
    )
    books_read_label.place(
        x=590, y=450
    )  # Adjust these coordinates for precise positioning

    # Settings Button - Placed just below the books read label
    logout_button = tk.Button(
        main_frame, text="LOGOUT", font=("Arial", 12), bg="#e0e000", fg="black"
    )
    logout_button.place(
        x=625, y=600
    )  # Adjust these coordinates for precise positioning


options_frame = tk.Frame(root, bg="#800000")

# Add logo to the top of options_frame
top_logo_image = Image.open("Images/pile.png")  # Path to your top logo image
top_logo_resized_image = top_logo_image.resize((100, 100), Image.Resampling.LANCZOS)
top_logo_photo = ImageTk.PhotoImage(top_logo_resized_image)

# Create label for top logo in options_frame
top_logo_label = tk.Label(options_frame, image=top_logo_photo, bg="#800000")
top_logo_label.image = top_logo_photo
top_logo_label.place(x=100, y=110, anchor="center")

# Add logo to the bottom of options_frame
bottom_logo_image = Image.open("Images/pile.png")  # Path to your bottom logo image
bottom_logo_resized_image = bottom_logo_image.resize(
    (100, 100), Image.Resampling.LANCZOS
)
bottom_logo_photo = ImageTk.PhotoImage(bottom_logo_resized_image)

# Create label for bottom logo in options_frame
bottom_logo_label = tk.Label(options_frame, image=bottom_logo_photo, bg="#800000")
bottom_logo_label.image = bottom_logo_photo
bottom_logo_label.place(x=100, y=680, anchor="center")  # Adjusted for window size

# Uniform width for all buttons
button_width = 16

home_btn = tk.Button(
    options_frame,
    text="Home",
    font=("Bold", 15),
    fg="#800000",
    bd=0,
    bg="#FFD700",
    width=button_width,
    command=lambda: indicate(home_indicate),
)
home_btn.place(x=10, y=300)

home_indicate = tk.Label(options_frame, text="", bg="#F0F0F0")
home_indicate.place(x=3, y=300, width=5, height=40)

mybooks_btn = tk.Button(
    options_frame,
    text="MyBooks",
    font=("Bold", 15),
    fg="#800000",
    bd=0,
    bg="#FFD700",
    width=button_width,
    command=lambda: indicate(mybooks_indicate),
)
mybooks_btn.place(x=10, y=350)

mybooks_indicate = tk.Label(options_frame, text="", bg="#F0F0F0")
mybooks_indicate.place(x=3, y=350, width=5, height=40)

leaderboards_btn = tk.Button(
    options_frame,
    text="Readerboards",
    font=("Bold", 15),
    fg="#800000",
    bd=0,
    bg="#FFD700",
    width=button_width,
    command=lambda: indicate(leaderboards_indicate),
)
leaderboards_btn.place(x=10, y=400)

leaderboards_indicate = tk.Label(options_frame, text="", bg="#F0F0F0")
leaderboards_indicate.place(x=3, y=400, width=5, height=40)

profile_btn = tk.Button(
    options_frame,
    text="Profile",
    font=("Bold", 15),
    fg="#800000",
    bd=0,
    bg="#FFD700",
    width=button_width,
    command=show_profile,
)
profile_btn.place(x=10, y=450)

profile_indicate = tk.Label(options_frame, text="", bg="#F0F0F0")
profile_indicate.place(x=3, y=450, width=5, height=40)

options_frame.pack(side=tk.LEFT, fill=tk.Y)
options_frame.pack_propagate(False)
options_frame.configure(width=200, height=400)

main_frame = tk.Frame(
    root, bg="#008080", highlightbackground="black", highlightthickness=2
)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
main_frame.pack_propagate(False)

root.mainloop()
