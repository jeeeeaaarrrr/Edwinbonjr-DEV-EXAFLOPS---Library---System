import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk

root = tk.Tk()
root.geometry("500x400")
root.title("Home")

# Load the icon image
icon_image = Image.open(
    "Images\\bookstrhophylogo-removebg-preview.png"
)  # Replace with the actual path to your icon file
icon_photo = ImageTk.PhotoImage(icon_image)

# Set the icon for the root window, which will show in the title bar and taskbar
root.iconphoto(False, icon_photo)


def hide_indicators():
    home_indicate.config(bg="#F0F0F0")
    mybooks_indicate.config(bg="#F0F0F0")
    leaderboards_indicate.config(bg="#F0F0F0")
    profile_indicate.config(bg="#F0F0F0")


def indicate(lb):
    hide_indicators()
    lb.config(bg="#158aff")


def create_leaderboard():
    # Clear any existing content in main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Change the background color to hunter green
    main_frame.config(bg="#008080")  # Hunter Green Color

    # Title label
    title_label = tk.Label(
        main_frame,
        text="🏆 Readerboard 🏆",
        font=("Helvetica", 24, "bold"),
        bg="#008080",  # Hunter Green Color
        fg="#ecf0f1",
    )
    title_label.pack(pady=20)

    # Table frame
    table_frame = tk.Frame(main_frame, bg="#34495e", bd=2, relief="solid")
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Create table headers
    headers = ["Rank", "Name", "Points"]
    for col_index, header in enumerate(headers):
        header_label = tk.Label(
            table_frame,
            text=header,
            font=("Helvetica", 14, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            padx=10,
            pady=5,
        )
        header_label.grid(row=0, column=col_index, sticky="nsew")

    # Add leaderboard data from 1 to 15 with points set to zero
    leaderboard_data = [(i, f"User{i}", 0) for i in range(1, 16)]

    # Populate table with data
    for row_index, (rank, name, score) in enumerate(leaderboard_data, start=1):
        rank_label = tk.Label(
            table_frame,
            text=str(rank),
            font=("Helvetica", 12),
            bg="#34495e",
            fg="#ecf0f1",
        )
        rank_label.grid(row=row_index, column=0, sticky="nsew")

        name_label = tk.Label(
            table_frame, text=name, font=("Helvetica", 12), bg="#34495e", fg="#ecf0f1"
        )
        name_label.grid(row=row_index, column=1, sticky="nsew")

        score_label = tk.Label(
            table_frame,
            text=str(score),
            font=("Helvetica", 12),
            bg="#34495e",
            fg="#ecf0f1",
        )
        score_label.grid(row=row_index, column=2, sticky="nsew")

    # Adjust column weights
    for col_index in range(len(headers)):
        table_frame.columnconfigure(col_index, weight=1)


options_frame = tk.Frame(root, bg="#800000")

# Add logo to the top of options_frame
top_logo_image = Image.open("Images/pile.png")  # Path to your top logo image
top_logo_resized_image = top_logo_image.resize((100, 100), Image.LANCZOS)
top_logo_photo = ImageTk.PhotoImage(top_logo_resized_image)

# Create label for top logo in options_frame
top_logo_label = tk.Label(options_frame, image=top_logo_photo, bg="#800000")
top_logo_label.image = top_logo_photo
top_logo_label.place(x=100, y=110, anchor="center")

# Add logo to the bottom of options_frame
bottom_logo_image = Image.open("Images/pile.png")  # Path to your bottom logo image
bottom_logo_resized_image = bottom_logo_image.resize((100, 100), Image.LANCZOS)
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
    command=lambda: [indicate(leaderboards_indicate), create_leaderboard()],
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
    command=lambda: indicate(profile_indicate),
)
profile_btn.place(x=10, y=450)

profile_indicate = tk.Label(options_frame, text="", bg="#F0F0F0")
profile_indicate.place(x=3, y=450, width=5, height=40)

options_frame.pack(side=tk.LEFT, fill=tk.Y)
options_frame.pack_propagate(False)
options_frame.configure(width=200, height=400)

main_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
main_frame.pack_propagate(False)

root.mainloop()
