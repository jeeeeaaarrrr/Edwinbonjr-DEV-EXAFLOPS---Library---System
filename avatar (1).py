import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  # You need to install Pillow: pip install Pillow


def browse_file():
    filename = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
    )
    if filename:
        file_label.config(text=filename)


def select_icon(event):
    global selected_icon, last_selected_icon_label

    # Reset the background color of the previously selected icon
    if last_selected_icon_label:
        last_selected_icon_label.config(bg="lightgray")

    # Store the image of the selected icon
    selected_icon = event.widget.cget("image")
    print(f"Selected icon: {selected_icon}")  # For debugging

    # Animation for selection
    original_borderwidth = event.widget.cget("borderwidth")
    event.widget.config(borderwidth=3, relief="raised", bg="#78081C")

    def revert_animation():
        event.widget.config(borderwidth=original_borderwidth, relief="groove")

    # After 300ms, revert borderwidth and relief, but keep the blue background
    event.widget.after(300, revert_animation)

    # Store the current label for next selection
    last_selected_icon_label = event.widget


def ok_action():
    if selected_icon:
        print(f"Confirmed icon: {selected_icon}")  # For debugging
        # Here you would handle what to do with the selected icon (e.g., use it, save it)
    else:
        print("No icon selected")


# Main window
root = tk.Tk()
root.title("Picture Upload")

# Frame for upload section
upload_frame = tk.Frame(root, padx=10, pady=10)
upload_frame.grid(row=0, column=0, sticky="ew")

# Label for upload section
tk.Label(upload_frame, text="Picture:").grid(row=0, column=0, sticky="w")

# Entry and Browse button
file_entry = tk.Entry(upload_frame, borderwidth=5, width=50)
file_entry.grid(row=1, column=0, sticky="w", padx=5, pady=5)
browse_button = tk.Button(upload_frame, text="Browse...", command=browse_file)
browse_button.grid(row=1, column=1, sticky="e")
ok_button = tk.Button(text="OK", fg="black", padx=5, command=ok_action)
ok_button.place(x=410, y=36)

# File selected label
file_label = tk.Label(root, text="")
file_label.grid(row=1, column=0, sticky="w", padx=10)

# Instructions
tk.Label(
    root,
    text="Your virtual face or picture. Maximum dimensions are 50x50 and the maximum size is 30 kB.",
    fg="grey",
).grid(row=2, column=0, sticky="w", padx=10)

# Frame for icons
icon_frame = tk.Frame(root, padx=10, pady=10)
icon_frame.grid(row=3, column=0, sticky="nsew")

# Configure the root to allow the icon_frame to expand
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

# Label for icon selection
tk.Label(icon_frame, text="Or simply select an icon:").grid(
    row=0, column=0, columnspan=4, sticky="w"
)

# Icons
icons = [
    "Images\\avatar1.png",
    "Images\\avatar2.png",
    "Images\\avatar3.png",
    "Images\\avatar4.png",
    "Images\\avatar6.png",
    "Images\\avatar7.png",
    "Images\\avatar8.png",
    "Images\\avatar9.png",
]

selected_icon = None  # To store the selected icon
last_selected_icon_label = None  # To keep track of which label was last selected

# Display icons
for i, icon in enumerate(icons):
    # Load the image
    try:
        img = Image.open(icon)
        # Resize to 150x150 for icons
        img = img.resize((150, 150), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(img)

        # Create a label to display the image with reduced frame size and make it selectable
        icon_label = tk.Label(
            icon_frame,
            image=tk_image,
            borderwidth=1,
            relief="groove",
            bg="lightgray",
        )
        icon_label.image = tk_image  # Keep a reference to prevent garbage collection
        icon_label.grid(row=(i // 4) + 1, column=i % 4, padx=2, pady=2, sticky="nsew")
        icon_label.bind("<Button-1>", select_icon)  # Bind left click to select icon

        # Configure rows and columns to expand
        icon_frame.grid_rowconfigure((i // 4) + 1, weight=1)
        icon_frame.grid_columnconfigure(i % 4, weight=1)
    except Exception as e:
        print(f"Error loading image {icon}: {e}")
        # If image loading fails, use a placeholder text with reduced frame
        icon_label = tk.Label(
            icon_frame,
            text=f"Error: {icon}",
            borderwidth=1,
            relief="groove",
            width=7,
            height=4,
            bg="lightgray",
        )
        icon_label.grid(row=(i // 4) + 1, column=i % 4, padx=2, pady=2, sticky="nsew")

root.mainloop()
