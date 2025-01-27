import tkinter as tk
from PIL import Image, ImageTk
import sqlite3

# Create or connect to the database
conn = sqlite3.connect("book_database.db")
c = conn.cursor()

# SQL command to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    cover_path TEXT
);
"""

# Create table if it doesn't exist
c.execute(create_table_sql)
conn.commit()

# Sample data insertion - only if the table is empty
c.execute("SELECT COUNT(*) FROM books")
count = c.fetchone()[0]

if count == 0:
    books = [
        (
            "The Information Superhighway Beyond the Internet",
            "Peter Otte",
            r"Images\\the information superhighway beyond the internet.png",
        ),
        (
            "Using Microsoft Office",
            "Unknown",
            r"Images\\Using Microsoft office.png",
        ),
        (
            "Word Processing Applications and Living Online",
            "Unknown",
            r"Images\Word processing.png",
        ),
        (
            "M.S DOS 5.0 - User's Guide and Reference Condensed Edition",
            "Unknown",
            r"Images\\M.S DOS 5.0 - User's Guide and Reference Condensed Edition.jpg",
        ),
        (
            "Microsoft Excel 2003 Proficiency in Electronic Spreadsheet",
            "Unknown",
            r"Images\\Microsoft Excel 2003 Proficiency in Electronic Spreadsheet.jpg",
        ),
        (
            "Management Information Systems: Managing the Digital Firm",
            "Kenneth C. Laudon, Jane P. Luadon",
            r"Images\\Management Information Systems Managing the Digital Firm.jpg",
        ),
        (
            "Photoshop Elements 3",
            "Craig Hoeschen",
            r"Images\\Photoshop Elements 3.jpg",
        ),
        (
            "Digital And Analog Controls",
            "Marvin A. Needler",
            r"Images\Digital And Analog Controls.jpg",
        ),
        (
            "Computer Software",
            "Ivan Flores",
            r"Images\\Computer Software.jpg",
        ),
        (
            "Introductions to Computers Concepts",
            "Juny Pilapil La Putt",
            r"Images\\Introductions to Computers Concepts.jpg",
        ),
        (
            "Data Structures and Algorithms",
            "Alfred V. Aho, John E. Hopcroft, Jeffry D. Ullman",
            r"Images\Data Structures and Algorithms.jpg",
        ),
        (
            "Modern Cable Television Technology",
            "Ciciora, Walter, Farmer, James and Large, David",
            r"Images\\Modern Cable Television Technology.jpg",
        ),
        (
            "Building PC for Dummies",
            "Mark Chambers",
            r"Images\Building PC for Dummies.jpg",
        ),
        (
            "Lotus Notes Release 4 for Dummies",
            "Londergan, Stephen and Freeland, Pat",
            r"Images\\Lotus Notes Release 4 for Dummies.jpg",
        ),
        (
            "Novell's Guide to NetWare 4.01 Networks",
            "Currid, Cheryl C. , Stephen Saxon",
            r"Images\\Novell's Guide to NetWare 4.01 Networks.jpg",
        ),
        (
            "Computer Literacy Program: Worktext in Computer Skills for Grade 6",
            "Unknown",
            r"Images\\Computer Literacy Program Worktext in Computer Skills for Grade 6.jpg",
        ),
        (
            "Understanding Structural Analysis",
            "Kassimali, Aslam",
            r"Images\\Understanding Structural Analysis.jpg",
        ),
        (
            "Computers  and Information Processing",
            "Unknown",
            r"Images\\Computers  and Information Processing.jpg",
        ),
        (
            "Sattelite Communication Systems",
            "Richharia, M.",
            r"Images\Sattelite Communication Systems.jpg",
        ),
        (
            "Recreation Programming: Designing and Staging Leisure Experiences",
            "Rossman, Robert J., and Schlatter, Barbara E.",
            r"Images\\Recreation Programming Designing and Staging Leisure Experiences.jpg",
        ),
        (
            "Antennas And Wave Propagation ",
            "Chris Harvey",
            r"Images\Antennas And Wave Propagation.jpg",
        ),
        (
            "Auditing IT Infrastructures for Compliance",
            "R.Johnson, M.Weiss, et al.",
            r"Images\Auditing IT Infrastructures for Compliance.jpg",
        ),
        (
            "Fundamentals of Internet of Things",
            "Farzin John Dian",
            r"Images\\Fundamentals of Internet of Things; For Students and Professionals.jpg",
        ),
        (
            "Digital Electronics",
            "R.Tokheim & P. Hoppe",
            r"Images\Digital Electronics.jpg",
        ),
        (
            "3D Printing for Energy Applications",
            "Pandey, Mukesh",
            r"Images\\3D Printing for Energy Applications.jpg",
        ),
        (
            "Deep Learning Applications",
            "Q.Xuan,Yun Xiang et al.",
            r"Images\Deep Learning Applications In Computer Vision, Signals, and Networks.jpg",
        ),
        (
            "Data Science for IOT Engineers",
            "P.G. Madhavan",
            r"Images\Data Science for IOT Engineers A Systems Analytics Approach.jpg",
        ),
        (
            "Cognitive Computing for Human Robot Interaction",
            "M.Mittal,R. Shah,et al.editor",
            r"Images\\Cognitive Computing for Human Robot Interaction Principles and Practices.jpg",
        ),
        (
            "Fundamentals of Electronic Materials and Devices",
            "Avik ghosh",
            r"Images\\Fundamentals of Electronic Materials and Devices A Gentle Introduction to the Quantum Classical World.jpg",
        ),
        (
            "Digital Electronics: A Practical Approach",
            "Kate Timberlake",
            r"Images\Digital Electronics A Practical Approach - Copy.jpg",
        ),
        (
            "A Framework for Marketing Management",
            "Kotler, Philip and Keler Kevin LAne",
            r"Images\A Framework for Marketing Management.jpg",
        ),
    ]

    for book in books:
        c.execute(
            "INSERT INTO books (title, author, cover_path) VALUES (?, ?, ?)", book
        )
    conn.commit()

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


def display_books():
    # Clear previous widgets in the main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Fetch books from database
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    for i, book in enumerate(books):
        book_id, title, author, cover_path = book
        # Calculate column and row for grid placement
        col = i % 2  # 0 or 1 for two columns
        row = i // 2  # integer division to get row
        add_book_item(title, author, cover_path, col, row)


def add_book_item(title, author, cover_path, col, row):
    book_frame = tk.Frame(main_frame, borderwidth=1, relief="solid")
    book_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    main_frame.grid_columnconfigure(0, weight=1)  # Allow columns to expand
    main_frame.grid_columnconfigure(1, weight=1)

    # Load and resize the image
    try:
        img = Image.open(cover_path)
        img = img.resize((100, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
    except IOError:
        print(f"Error: Could not open image at {cover_path}")
        return

    # Display cover image
    cover_label = tk.Label(book_frame, image=photo)
    cover_label.image = photo  # Keep a reference!
    cover_label.pack(side="left")

    # Display book info
    info_frame = tk.Frame(book_frame)
    info_frame.pack(side="left", padx=23)

    title_label = tk.Label(info_frame, text=title, font=("Helvetica", 12, "bold"))
    title_label.pack(anchor="w")

    author_label = tk.Label(info_frame, text=f"by {author}")
    author_label.pack(anchor="w")


options_frame = tk.Frame(root, bg="#800000")

# Add logo to the top of options_frame
top_logo_image = Image.open("Images/pile.png")  # Path to your top logo image
top_logo_resized_image = top_logo_image.resize((100, 100), Image.LANCZOS)
top_logo_photo = ImageTk.PhotoImage(top_logo_resized_image)

top_logo_label = tk.Label(options_frame, image=top_logo_photo, bg="#800000")
top_logo_label.image = top_logo_photo
top_logo_label.place(x=100, y=110, anchor="center")

# Add logo to the bottom of options_frame
bottom_logo_image = Image.open("Images/pile.png")  # Path to your bottom logo image
bottom_logo_resized_image = bottom_logo_image.resize((100, 100), Image.LANCZOS)
bottom_logo_photo = ImageTk.PhotoImage(bottom_logo_resized_image)

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
    command=lambda: [indicate(mybooks_indicate), display_books()],
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

# Scrollable setup for main_frame
scrollable_frame = tk.Frame(root)
scrollable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a canvas for scrolling
canvas = tk.Canvas(scrollable_frame)
scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas which will contain the books
main_frame = tk.Frame(canvas, highlightbackground="black", highlightthickness=2)

# Update scroll region when the frame changes
main_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Place the canvas and scrollbar in the scrollable_frame
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Create a window in the canvas which holds the main_frame
canvas.create_window((0, 0), window=main_frame, anchor="nw")

# Bind mouse wheel for scrolling
canvas.bind_all(
    "<MouseWheel>",
    lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"),
)

root.mainloop()

# Close the database connection when done
conn.close()
