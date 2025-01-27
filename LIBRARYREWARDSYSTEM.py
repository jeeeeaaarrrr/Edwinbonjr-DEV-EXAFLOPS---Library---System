import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import os

login_frame = None
admin_login_frame = None
sign_up_frame = None
selected_icon_filename = None
current_user_id = None
current_points = 0
books_read_count = 0
read_books = set()  # Track books read in the current session


# Custom style for buttons with rounded corners
class RoundButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(relief="flat", borderwidth=0)


def setup_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Ensure the users table exists with the points column
    c.execute(
        """CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, 
                  password TEXT, 
                  avatar TEXT DEFAULT NULL,
                  selected_icon_filename TEXT DEFAULT NULL,
                  points INTEGER DEFAULT 0)"""
    )

    # In case the table already exists without the points column, add it
    try:
        c.execute("ALTER TABLE users ADD COLUMN points INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        # The column already exists, so we catch the error silently
        pass

    # Create or ensure the leaderboards table exists
    c.execute(
        """CREATE TABLE IF NOT EXISTS leaderboards 
                 (username TEXT PRIMARY KEY, 
                  points INTEGER DEFAULT 0)"""
    )

    # Create or ensure the read_books table exists with book_key
    c.execute(
        """CREATE TABLE IF NOT EXISTS read_books 
                 (username TEXT, 
                  book_key TEXT, 
                  PRIMARY KEY (username, book_key),
                  FOREIGN KEY (username) REFERENCES users(username))"""
    )

    # If the table exists but book_key does not, add it
    try:
        c.execute("SELECT book_key FROM read_books LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("ALTER TABLE read_books ADD COLUMN book_key TEXT")

    conn.commit()
    conn.close()

    # Optionally, ensure all existing users have a points value (if not already set)
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET points = 0 WHERE points IS NULL")
    conn.commit()
    conn.close()


def register_user():
    username = username_entry.get()
    password = password_entry.get()
    reenter_password = reenterpassword_entry.get()

    if username and password and reenter_password:
        if password == reenter_password:
            try:
                conn = sqlite3.connect("users.db")
                c = conn.cursor()

                c.execute("SELECT * FROM users WHERE username = ?", (username,))
                if c.fetchone() is None:
                    avatar = selected_icon_filename if selected_icon_filename else None

                    c.execute(
                        """INSERT INTO users (username, password, avatar, selected_icon_filename, points) 
                                VALUES (?, ?, ?, ?, 0)""",
                        (username, password, avatar, selected_icon_filename),
                    )
                    conn.commit()
                    messagebox.showinfo("Success", "Registration successful!")
                    conn.close()

                    book_conn = sqlite3.connect("book_database.db")
                    book_c = book_conn.cursor()
                    create_table_sql = """
                    CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        cover_path TEXT
                    );
                    """
                    book_c.execute(create_table_sql)
                    book_conn.commit()

                    book_c.execute("SELECT COUNT(*) FROM books")
                    count = book_c.fetchone()[0]

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
                            book_c.execute(
                                "INSERT INTO books (title, author, cover_path) VALUES (?, ?, ?)",
                                book,
                            )
                        book_conn.commit()

                    book_conn.close()

                    global current_user_id
                    current_user_id = username
                    setup_new_interface()
                    return True
                else:
                    messagebox.showerror("Error", "Username already exists!")
                    conn.close()
                    return False
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                return False
            finally:
                if conn:
                    conn.close()
        else:
            messagebox.showerror("Error", "Passwords do not match!")
            return False
    else:
        messagebox.showerror("Error", "Please fill in all fields.")
        return False


# Function to toggle password visibility
def toggle_password_visibility(entry, var, check):
    if var.get():
        entry.config(show="")
        check.config(selectcolor="blue")
    else:
        entry.config(show="*")
        check.config(selectcolor="white")


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
        user = c.fetchone()
        if user:
            global selected_icon_filename, current_user_id, current_points, books_read_count
            try:
                selected_icon_filename = user[3] if len(user) > 3 else None
                current_user_id = username
                current_points = user[4] if len(user) > 4 else 0  # Points from database
                books_read_count = (
                    current_points // 10
                )  # Assuming each book read gives 10 points

                # Load read books for this user
                c.execute(
                    "SELECT book_key FROM read_books WHERE username = ?", (username,)
                )
                read_books.clear()
                for book in c.fetchall():
                    read_books.add(book[0])

            except IndexError:
                selected_icon_filename = None
                current_points = 0
                books_read_count = 0
                print(
                    "Warning: selected_icon_filename or points not found in database."
                )

            messagebox.showinfo("Success", "Login successful!")
            setup_new_interface()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
        conn.close()
    else:
        messagebox.showerror("Error", "Please enter both username and password.")


def on_login_student():
    global login_frame

    for widget in root.winfo_children():
        widget.place_forget()

    if login_frame is None or not login_frame.winfo_exists():
        login_frame = tk.Frame(root, bg="maroon")

        username_label = tk.Label(
            login_frame,
            text="PUP ID:",
            bg="maroon",
            fg="white",
            font=("Helvetica", 14, "bold"),
        )
        username_label.pack(pady=10)

        global username_entry
        username_entry = tk.Entry(
            login_frame, borderwidth=5, width=30, font=("Helvetica", 12)
        )
        username_entry.pack(pady=10)

        password_label = tk.Label(
            login_frame,
            text="Password:",
            bg="maroon",
            fg="white",
            font=("Helvetica", 14, "bold"),
        )
        password_label.pack(pady=10)

        global password_entry
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
            selectcolor="white",
            activebackground="darkred",
            indicatoron=1,
            height=1,
            width=15,
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

    login_frame.pack(fill="both", expand=True)
    login_frame.lift()


def on_login_admin():
    global admin_login_frame

    for widget in root.winfo_children():
        widget.place_forget()

    if admin_login_frame is None or not admin_login_frame.winfo_exists():
        admin_login_frame = tk.Frame(root, bg="maroon")

        admin_username_label = tk.Label(
            admin_login_frame,
            text="Admin Username:",
            bg="maroon",
            fg="white",
            font=("Helvetica", 14, "bold"),
        )
        admin_username_label.pack(pady=10)

        global admin_username_entry
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

        global admin_password_entry
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
            selectcolor="white",
            activebackground="darkred",
            indicatoron=1,
            height=1,
            width=15,
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
    global sign_up_frame, username_entry, password_entry, reenterpassword_entry
    for widget in root.winfo_children():
        widget.place_forget()

    if sign_up_frame is None or not sign_up_frame.winfo_exists():
        sign_up_frame = tk.Frame(root, bg="maroon")
        sign_up_frame.pack(fill="both", expand=True)
        sign_up_frame.lift()

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
            selectcolor="white",
            activebackground="darkred",
            indicatoron=1,
            height=1,
            width=15,
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
            selectcolor="white",
            activebackground="darkred",
            indicatoron=1,
            height=1,
            width=15,
        )
        reenter_show_password_check.pack(pady=5, anchor="c")

        sign_up_button = tk.Button(
            sign_up_frame,
            text="Sign Up",
            command=check_username_and_proceed,
            bg="#FFD700",
            fg="maroon",
            font=("Helvetica", 12),
            width=10,
            height=1,
        )
        sign_up_button.pack(pady=10)

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


def check_username_and_proceed():
    username = username_entry.get()
    password = password_entry.get()
    reenter_password = reenterpassword_entry.get()

    if username and password and reenter_password:
        if password == reenter_password:
            try:
                conn = sqlite3.connect("users.db")
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username = ?", (username,))
                if c.fetchone() is None:
                    show_icon_selection()
                else:
                    messagebox.showerror("Error", "Username already exists!")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
            finally:
                if conn:
                    conn.close()
        else:
            messagebox.showerror("Error", "Passwords do not match!")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")


def show_icon_selection():
    global sign_up_frame, last_selected_icon_label

    last_selected_icon_label = None
    for child in sign_up_frame.winfo_children():
        child.pack_forget()

    tk.Label(
        sign_up_frame,
        text="Select an icon:",
        bg="maroon",
        fg="white",
        font=("Helvetica", 14, "bold"),
    ).pack(pady=10)

    icon_frame = tk.Frame(sign_up_frame, bg="maroon")
    icon_frame.pack()

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

    for i, icon in enumerate(icons):
        try:
            img = Image.open(icon)
            img = img.resize((100, 100), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(img)

            icon_label = tk.Label(
                icon_frame,
                image=tk_image,
                borderwidth=1,
                relief="groove",
                bg="lightgray",
            )
            icon_label.image = tk_image
            icon_label.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            icon_label.bind(
                "<Button-1>",
                lambda event, img=tk_image, icon_path=icon: select_icon(
                    event, img, icon_path
                ),
            )
        except Exception as e:
            print(f"Error loading image {icon}: {e}")

    ok_button = tk.Button(
        sign_up_frame,
        text="OK",
        command=register_user,
        bg="#FFD700",
        fg="maroon",
        font=("Helvetica", 12),
        width=10,
        height=1,
    )
    ok_button.pack(pady=10)


def select_icon(event, img, icon_path):
    global selected_icon_filename, last_selected_icon_label

    if last_selected_icon_label:
        last_selected_icon_label.config(bg="lightgray")

    selected_icon_filename = icon_path
    print(f"Selected icon filename: {selected_icon_filename}")

    original_borderwidth = event.widget.cget("borderwidth")
    event.widget.config(borderwidth=3, relief="raised", bg="#78081C")

    def revert_animation():
        event.widget.config(borderwidth=original_borderwidth, relief="groove")

    event.widget.after(300, revert_animation)
    last_selected_icon_label = event.widget


def go_back():
    global login_frame, admin_login_frame, sign_up_frame

    if login_frame:
        login_frame.pack_forget()
    if admin_login_frame:
        admin_login_frame.pack_forget()
    if sign_up_frame:
        sign_up_frame.pack_forget()

    setup_initial_interface()


def setup_initial_interface():
    global background_label, header_frame, login_student_button, login_admin_button, sign_up_button

    for widget in root.winfo_children():
        widget.destroy()

    try:
        background_image = Image.open(r"Images/download.png").resize(
            (1600, 1600), Image.LANCZOS
        )
        background_photo = ImageTk.PhotoImage(background_image)
    except FileNotFoundError:
        print("Error: Background image not found. Please check the file path.")
        background_photo = None

    background_label = tk.Label(root, image=background_photo)
    if background_photo:
        background_label.image = background_photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    header_frame = tk.Frame(root, bg="#800000", height=300)
    header_frame.pack(fill="x")

    canvas = tk.Canvas(
        header_frame, width=100, height=100, bg="#800000", highlightthickness=0
    )
    canvas.pack(pady=20)

    try:
        logo_image = Image.open(r"Images/puplogo.png").resize((100, 100))
        logo = ImageTk.PhotoImage(logo_image)
        canvas.create_image(50, 50, image=logo)
        canvas.image = logo
    except FileNotFoundError:
        print("Error: Logo image not found. Please check the file path.")

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


def logout():
    global login_frame, admin_login_frame, sign_up_frame
    for widget in root.winfo_children():
        widget.destroy()

    login_frame = None
    admin_login_frame = None
    sign_up_frame = None

    root.geometry("500x650")
    root.update_idletasks()

    root.title("Library System")
    setup_initial_interface()

    global selected_icon_filename, current_user_id, current_points, books_read_count, read_books
    selected_icon_filename = None
    current_user_id = None
    current_points = 0
    books_read_count = 0
    read_books = set()  # Reset read books set on logout


# Initialize the Tkinter app
root = tk.Tk()
root.title("Library System")
root.geometry("500x650")

setup_database()


def setup_new_interface():
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("800x600")
    root.title("Pup Library System")
    root.update_idletasks()  # Ensure the window size change is reflected

    try:
        icon_image = Image.open("Images\\bookstrhophylogo-removebg-preview.png")
        icon_photo = ImageTk.PhotoImage(icon_image)
        root.iconphoto(False, icon_photo)
    except FileNotFoundError:
        print("Error: Icon image not found. Please check the file path.")

    def hide_indicators():
        home_indicate.config(bg="#F0F0F0")
        books_indicate.config(bg="#F0F0F0")
        leaderboards_indicate.config(bg="#F0F0F0")
        profile_indicate.config(bg="#F0F0F0")

    def indicate(lb):
        hide_indicators()
        lb.config(bg="#158aff")

    def display_home():
        for widget in home_frame.winfo_children():
            widget.destroy()
        home_frame.config(bg="white")

        try:
            original_image = Image.open(r"Images\Seading-Quotes-1.jpg")
            resized_image = original_image.resize((1400, 800), Image.LANCZOS)
            main_frame_photo = ImageTk.PhotoImage(resized_image)

            main_frame_photo_label = tk.Label(home_frame, image=main_frame_photo)
            main_frame_photo_label.image = main_frame_photo
            main_frame_photo_label.pack(fill=tk.BOTH, expand=True)
        except IOError:
            print("Error: Could not open home image at the specified path.")

        home_frame.pack(fill=tk.BOTH, expand=True)
        indicate(
            home_indicate
        )  # <--- Add this line to indicate home when home is displayed

    def display_books():
        for widget in books_frame.winfo_children():
            widget.destroy()
        books_frame.config(bg="white")

        book_conn = sqlite3.connect("book_database.db")
        book_c = book_conn.cursor()
        book_c.execute("SELECT * FROM books")
        books = book_c.fetchall()
        for i, book in enumerate(books):
            book_id, title, author, cover_path = book
            col = i % 2
            row = i // 2
            add_book_item(title, author, cover_path, col, row, books_frame)

        book_conn.close()
        update_books_canvas()

        books_scroll_frame.pack(fill=tk.BOTH, expand=True)

    def add_book_item(title, author, cover_path, col, row, frame):
        book_frame = tk.Frame(frame, borderwidth=2, relief="solid")
        book_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        book_key = f"{title}{author}"  # Use the same key mechanism

        try:
            img = Image.open(cover_path)
            img = img.resize((100, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        except IOError:
            print(f"Error: Could not open image at {cover_path}")
            return

        cover_label = tk.Label(book_frame, image=photo)
        cover_label.image = photo
        cover_label.pack(side="left")

        info_frame = tk.Frame(book_frame)
        info_frame.pack(side="left", padx=22, fill="x", expand=True)

        title_label = tk.Label(
            info_frame, text=title, font=("Helvetica", 12, "bold"), fg="black"
        )
        title_label.pack(anchor="w")

        author_label = tk.Label(info_frame, text=f"by {author}", fg="black")
        author_label.pack(anchor="w")

        button_text = tk.StringVar()
        button_text.set("Read" if book_key in read_books else "Add To Read Books")

        def change_button_text():
            button_text.set("Read")
            add_button.config(state="disabled", fg="black", bg="lightgreen")
            read_books.add(book_key)  # Add to session memory

            # Update database
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            try:
                c.execute(
                    "INSERT OR REPLACE INTO read_books (username, book_key) VALUES (?, ?)",
                    (current_user_id, book_key),
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error updating read books: {str(e)}")
            finally:
                conn.close()

        add_button = tk.Button(
            info_frame,
            textvariable=button_text,
            command=lambda: (
                [add_to_read_books(title, author), change_button_text()]
                if button_text.get() != "Read"
                else None
            ),
            bg="red" if button_text.get() != "Read" else "lightgreen",
            fg="white" if button_text.get() != "Read" else "black",
            font=("Helvetica", 10),
            state=tk.DISABLED if button_text.get() == "Read" else tk.NORMAL,
        )
        add_button.pack(pady=5, fill="x")

    def add_to_read_books(title, author):
        global current_points, books_read_count

        book_key = f"{title}{author}"  # Create a unique key for each book
        if book_key not in read_books:
            books_read_count += 1
            current_points += 10
            read_books.add(book_key)

            # Update database
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            try:
                c.execute(
                    "UPDATE users SET points = ? WHERE username = ?",
                    (current_points, current_user_id),
                )
                c.execute(
                    "INSERT OR REPLACE INTO read_books (username, book_key) VALUES (?, ?)",
                    (current_user_id, book_key),
                )
                conn.commit()
            except sqlite3.Error as e:
                messagebox.showerror(
                    "Database Error",
                    f"An error occurred while updating points: {str(e)}",
                )
            finally:
                conn.close()

            messagebox.showinfo(
                "Book Added",
                f"'{title}' added to your read list. Total books read: {books_read_count}",
            )

    def create_leaderboard():
        for widget in leaderboard_frame.winfo_children():
            widget.destroy()
        leaderboard_frame.config(bg="#008080")

        title_label = tk.Label(
            leaderboard_frame,
            text="🏆 Readerboard 🏆",
            font=("Helvetica", 45, "bold"),
            bg="#008080",
            fg="gold",
        )
        title_label.pack(pady=20)

        table_frame = tk.Frame(leaderboard_frame, bg="#34495e", bd=3, relief="solid")
        table_frame.pack(pady=125, padx=152, fill="both", expand=True)

        headers = ["Rank", "Name", "Points"]
        for col_index, header in enumerate(headers):
            header_label = tk.Label(
                table_frame,
                text=header,
                font=("Helvetica", 20, "bold"),
                bg="#34495e",
                fg="gold",
                padx=130,
                pady=10,
            )
            header_label.grid(row=0, column=col_index, sticky="nsew")

        # Fetch data from the leaderboard, joining with read_books to ensure only users with read books are listed
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute(
            """
            SELECT u.username, u.points 
            FROM users u
            JOIN read_books rb ON u.username = rb.username
            GROUP BY u.username, u.points 
            ORDER BY u.points DESC LIMIT 15
        """
        )
        leaderboard_data = c.fetchall()
        conn.close()

        # If there are no users with read books, show default data
        if not leaderboard_data:
            leaderboard_data = [(f"User{i+1}", 0) for i in range(15)]

        for row_index, (name, score) in enumerate(leaderboard_data, start=1):
            rank_label = tk.Label(
                table_frame,
                text=str(row_index),
                font=("Helvetica", 12),
                bg="#34495e",
                fg="#ecf0f1",
            )
            rank_label.grid(row=row_index, column=0, sticky="nsew")

            name_label = tk.Label(
                table_frame,
                text=name,
                font=("Helvetica", 12),
                bg="#34495e",
                fg="#ecf0f1",
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

        for col_index in range(len(headers)):
            table_frame.columnconfigure(col_index, weight=1)

        leaderboard_frame.pack(fill=tk.BOTH, expand=True)

    def on_mousewheel(event):
        if event.num == 4 or event.delta > 0:
            books_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            books_canvas.yview_scroll(1, "units")

    def show_profile():
        for widget in profile_frame.winfo_children():
            widget.destroy()
        profile_frame.config(bg="teal")

        try:
            # Force an update before placing widgets
            profile_frame.pack(fill=tk.BOTH, expand=True)
            profile_frame.update_idletasks()

            frame_width = profile_frame.winfo_width()
            frame_height = profile_frame.winfo_height()

            profile_image = Image.open(
                selected_icon_filename
                if selected_icon_filename
                else "Images\\avatar1.png"
            )
            profile_image = profile_image.resize((300, 300), Image.LANCZOS)
            profile_photo = ImageTk.PhotoImage(profile_image)

            profile_label = tk.Label(profile_frame, image=profile_photo, bg="teal")
            profile_label.image = profile_photo
            profile_label.place(x=frame_width // 2 - 200, y=frame_height // 8)

            name_label = tk.Label(
                profile_frame,
                text=current_user_id,
                font=("Arial", 20, "bold"),
                fg="white",
                bg="teal",
            )
            name_label.place(
                x=frame_width // 2 - name_label.winfo_reqwidth() // 2 - 50,
                y=frame_height // 2 + 20,
            )

            books_read_label = tk.Label(
                profile_frame,
                text=f"▶ {books_read_count} Books Read ◀",
                font=("Arial", 14),
                fg="red",
                bg="teal",
            )
            books_read_label.place(
                x=frame_width // 2 - books_read_label.winfo_reqwidth() // 2 - 50,
                y=frame_height // 2 + 70,
            )

            points_label = tk.Label(
                profile_frame,
                text=f"Points: {current_points}",
                font=("Arial", 14),
                fg="gold",
                bg="teal",
            )
            points_label.place(
                x=frame_width // 2 - points_label.winfo_reqwidth() // 2 - 50,
                y=frame_height // 2 + 110,
            )

            logout_button = tk.Button(
                profile_frame,
                text="LOGOUT",
                font=("Arial", 12),
                bg="#e0e000",
                fg="black",
                command=logout,
            )
            logout_button.place(
                x=frame_width // 2 - logout_button.winfo_reqwidth() // 2 - 50,
                y=frame_height * 3 // 4,
            )
        except IOError:
            print("Error: Profile image not found. Please check the file path.")

    options_frame = tk.Frame(root, bg="#800000")
    options_frame.pack(side=tk.LEFT, fill=tk.Y)
    options_frame.pack_propagate(False)
    options_frame.configure(width=200, height=400)

    try:
        top_logo_image = Image.open("Images/pile.png")
        top_logo_resized_image = top_logo_image.resize((100, 100), Image.LANCZOS)
        top_logo_photo = ImageTk.PhotoImage(top_logo_resized_image)
        top_logo_label = tk.Label(options_frame, image=top_logo_photo, bg="#800000")
        top_logo_label.image = top_logo_photo
        top_logo_label.place(x=100, y=110, anchor="center")

        bottom_logo_image = Image.open("Images/pile.png")
        bottom_logo_resized_image = bottom_logo_image.resize((100, 100), Image.LANCZOS)
        bottom_logo_photo = ImageTk.PhotoImage(bottom_logo_resized_image)
        bottom_logo_label = tk.Label(
            options_frame, image=bottom_logo_photo, bg="#800000"
        )
        bottom_logo_label.image = bottom_logo_photo
        bottom_logo_label.place(x=100, y=680, anchor="center")
    except FileNotFoundError:
        print("Error: Logo images not found. Please check the file paths.")

    button_width = 16

    home_btn = tk.Button(
        options_frame,
        text="Home",
        font=("Bold", 15),
        fg="#800000",
        bd=0,
        bg="#FFD700",
        width=button_width,
        command=lambda: [hide_all_frames(), indicate(home_indicate), display_home()],
    )
    home_btn.place(x=10, y=300)

    home_indicate = tk.Label(options_frame, text="", bg="#F0F0F0")
    home_indicate.place(x=3, y=300, width=5, height=40)

    books_btn = tk.Button(
        options_frame,
        text="Books",
        font=("Bold", 15),
        fg="#800000",
        bd=0,
        bg="#FFD700",
        width=button_width,
        command=lambda: [hide_all_frames(), indicate(books_indicate), display_books()],
    )
    books_btn.place(x=10, y=350)

    books_indicate = tk.Label(options_frame, text="", bg="#F0F0F0")
    books_indicate.place(x=3, y=350, width=5, height=40)

    leaderboards_btn = tk.Button(
        options_frame,
        text="Readerboards",
        font=("Bold", 15),
        fg="#800000",
        bd=0,
        bg="#FFD700",
        width=button_width,
        command=lambda: [
            hide_all_frames(),
            indicate(leaderboards_indicate),
            create_leaderboard(),
        ],
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
        command=lambda: [hide_all_frames(), indicate(profile_indicate), show_profile()],
    )
    profile_btn.place(x=10, y=450)

    profile_indicate = tk.Label(options_frame, text="", bg="#F0F0F0")
    profile_indicate.place(x=3, y=450, width=5, height=40)

    content_frame = tk.Frame(root)
    content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    global home_frame, books_scroll_frame, books_canvas, books_frame, leaderboard_frame, profile_frame

    home_frame = tk.Frame(content_frame, bg="white")
    books_scroll_frame = tk.Frame(content_frame)
    books_canvas = tk.Canvas(books_scroll_frame)
    books_scrollbar = tk.Scrollbar(
        books_scroll_frame, orient="vertical", command=books_canvas.yview
    )
    books_frame = tk.Frame(books_canvas)
    leaderboard_frame = tk.Frame(content_frame, bg="#008080")
    profile_frame = tk.Frame(content_frame, bg="teal")

    books_frame.bind(
        "<Configure>",
        lambda e: books_canvas.configure(scrollregion=books_canvas.bbox("all")),
    )
    books_canvas.create_window((0, 0), window=books_frame, anchor="nw")
    books_canvas.configure(yscrollcommand=books_scrollbar.set)

    books_canvas.pack(side="left", fill="both", expand=True)
    books_scrollbar.pack(side="right", fill="y")

    # Add these bindings for mousewheel scrolling
    books_canvas.bind_all("<MouseWheel>", on_mousewheel)
    books_canvas.bind_all("<Button-4>", on_mousewheel)
    # For Linux or Windows with different behavior
    books_canvas.bind_all("<Button-5>", on_mousewheel)
    books_canvas.bind("<Button-1>", lambda event: books_canvas.focus_set())

    def hide_all_frames():
        for frame in [home_frame, books_scroll_frame, leaderboard_frame, profile_frame]:
            frame.pack_forget()

    def update_books_canvas():
        books_frame.update_idletasks()
        books_canvas.configure(scrollregion=books_canvas.bbox("all"))

    # Initially display the home screen
    display_home()


setup_initial_interface()
root.mainloop()
