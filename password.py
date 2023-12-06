import sqlite3
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox

# Connect to the database
conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

# Create table to store passwords if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Function to securely hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add a password
def add_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    hashed_password = hash_password(password)
    
    cursor.execute('''
        INSERT INTO passwords (website, username, password)
        VALUES (?, ?, ?)
    ''', (website, username, hashed_password))
    conn.commit()
    messagebox.showinfo("Success", "Password added successfully.")

# Function to retrieve passwords and usernames for a given website
def get_password():
    website = website_entry.get()

    cursor.execute('''
        SELECT username, password FROM passwords
        WHERE website = ?
    ''', (website,))
    results = cursor.fetchall()

    if results:
        password_list = "\n".join([f"Username: {result[0]}, Password: {result[1]}" for result in results])
        messagebox.showinfo("Passwords", f"Retrieved passwords for {website}:\n{password_list}")
    else:
        messagebox.showwarning("Password not found", "No passwords found for this website.")

# GUI Setup
root = tk.Tk()
root.title("Password Manager")

style = ttk.Style()
style.theme_use("clam")  # Change the theme to your liking

main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0)

website_label = ttk.Label(main_frame, text="Website:")
website_label.grid(row=0, column=0, padx=5, pady=5)
website_entry = ttk.Entry(main_frame)
website_entry.grid(row=0, column=1, padx=5, pady=5)

username_label = ttk.Label(main_frame, text="Username:")
username_label.grid(row=1, column=0, padx=5, pady=5)
username_entry = ttk.Entry(main_frame)
username_entry.grid(row=1, column=1, padx=5, pady=5)

password_label = ttk.Label(main_frame, text="Password:")
password_label.grid(row=2, column=0, padx=5, pady=5)
password_entry = ttk.Entry(main_frame, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = ttk.Button(main_frame, text="Add Password", command=add_password)
add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

get_button = ttk.Button(main_frame, text="Get Passwords", command=get_password)
get_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

root.mainloop()

# Close the connection
conn.close()
