import mysql.connector
import random
import string
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("400x400")

        self.setup_database()

        self.website_label = tk.Label(root, text="Website:")
        self.website_entry = tk.Entry(root)
        self.username_label = tk.Label(root, text="Username:")
        self.username_entry = tk.Entry(root)
        self.password_label = tk.Label(root, text="Password:")
        self.password_entry = tk.Entry(root)
        self.generate_button = tk.Button(root, text="Generate Password", command=self.generate_password)
        self.save_button = tk.Button(root, text="Save Password", command=self.save_password)
        self.view_button = tk.Button(root, text="View Passwords", command=self.view_passwords)
        self.password_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)

        self.website_label.pack()
        self.website_entry.pack()
        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.generate_button.pack()
        self.save_button.pack()
        self.view_button.pack()
        self.password_display.pack()

    def setup_database(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Phantom@123",
                database="passwordstorage"
            )
            self.cursor = self.connection.cursor()

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                website VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
            """)

            self.connection.close()
        except Exception as e:
            self.result_label.config(text="Error: " + str(e))

    def generate_password(self):
        password_length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(password_length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def save_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not website or not username or not password:
            self.result_label.config(text="Please fill in all fields")
            return

        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Phantom@123",
                database="passwordstorage"
            )
            self.cursor = self.connection.cursor()

            query = "INSERT INTO passwords (website, username, password) VALUES (%s, %s, %s)"
            values = (website, username, password)
            self.cursor.execute(query, values)
            self.connection.commit()
            self.connection.close()
            self.result_label.config(text="Password saved successfully")

        except Exception as e:
            self.result_label.config(text="Error: " + str(e))

    def view_passwords(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Phantom@123",
            database="passwordstorage"
        )
        self.cursor = self.connection.cursor()

        self.cursor.execute("SELECT website, username, password FROM passwords")
        passwords = self.cursor.fetchall()

        if not passwords:
            result_label = tk.Label(self.root, text="No passwords found.")
            result_label.pack()
        else:
            view_window = tk.Toplevel(self.root)
            view_window.title("View Passwords")
            view_window.geometry("600x400")

            for password in passwords:
                website = password[0]
                username = password[1]
                password_text = password[2]

                password_frame = tk.Frame(view_window)
                password_frame.pack()

                website_label = tk.Label(password_frame, text=f"Website: {website}")
                website_label.pack()

                username_label = tk.Label(password_frame, text=f"Username: {username}")
                username_label.pack()

                password_label = tk.Label(password_frame, text=f"Password: {password_text}")
                password_label.pack()

        self.connection.close()

    def close_window(self):
        self.root.destroy()

    def generate_random_password(self):
        password_length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(password_length))
        return password

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
