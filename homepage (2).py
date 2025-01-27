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
    command=lambda: indicate(profile_indicate),
)
profile_btn.place(x=10, y=450)

profile_indicate = tk.Label(options_frame, text="", bg="#F0F0F0")
profile_indicate.place(x=3, y=450, width=5, height=40)

options_frame.pack(side=tk.LEFT, fill=tk.Y)
options_frame.pack_propagate(False)
options_frame.configure(width=200, height=400)

main_frame = tk.Frame(root, highlightbackground="black", highlightthickness=2)

# Adjust image size to fit within the window
original_image = Image.open("Images\\Seading-Quotes-1.jpg")
resized_image = original_image.resize((1400, 800), Image.LANCZOS)  # Adjust size to fit
main_frame_photo = ImageTk.PhotoImage(resized_image)

main_frame_photo_label = tk.Label(main_frame, image=main_frame_photo)
main_frame_photo_label.image = main_frame_photo
main_frame_photo_label.pack(pady=0)

main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
main_frame.pack_propagate(False)

root.mainloop()
