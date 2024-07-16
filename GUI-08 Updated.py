import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class WelcomeWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BankSwift")
        self.root.geometry("400x400")
        self.root.configure(bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        create_account_btn = tk.Button(self.root, text="Create Account", command=self.open_create_account, bg="#4CAF50", fg="white", padx=20, pady=10)
        create_account_btn.place(relx=0.5, rely=0.4, anchor="center")

        login_btn = tk.Button(self.root, text="Login", command=self.open_login, bg="#2196F3", fg="white", padx=20, pady=10)
        login_btn.place(relx=0.5, rely=0.6, anchor="center")

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        about_menu = tk.Menu(menubar)
        menubar.add_cascade(label="About Us", menu=about_menu)
        about_menu.add_command(label="About Us")

        contact_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Contact Us", menu=contact_menu)
        contact_menu.add_command(label="Contact Us")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        self.root.destroy()

    def open_create_account(self):
        self.root.withdraw()
        CreateAccountWindow(self)

    def open_login(self):
        self.root.withdraw()
        LoginWindow(self)


class CreateAccountWindow:
    def __init__(self, welcome_window):
        self.welcome_window = welcome_window
        self.create_account = tk.Toplevel()
        self.create_account.title("Create Account")
        self.create_account.geometry("600x600")
        self.create_account.configure(bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        name_label = tk.Label(self.create_account, text="Name:", bg="#f0f0f0")
        name_label.place(relx=0.1, rely=0.1)
        self.name_entry = tk.Entry(self.create_account)
        self.name_entry.place(relx=0.3, rely=0.1)

        surname_label = tk.Label(self.create_account, text="Surname:", bg="#f0f0f0")
        surname_label.place(relx=0.1, rely=0.15)
        self.surname_entry = tk.Entry(self.create_account)
        self.surname_entry.place(relx=0.3, rely=0.15)

        id_label = tk.Label(self.create_account, text="ID No.:", bg="#f0f0f0")
        id_label.place(relx=0.1, rely=0.2)
        self.id_entry = tk.Entry(self.create_account)
        self.id_entry.place(relx=0.3, rely=0.2)

        phone_label = tk.Label(self.create_account, text="Phone:", bg="#f0f0f0")
        phone_label.place(relx=0.1, rely=0.25)
        self.phone_entry = tk.Entry(self.create_account)
        self.phone_entry.place(relx=0.3, rely=0.25)

        email_label = tk.Label(self.create_account, text="Email:", bg="#f0f0f0")
        email_label.place(relx=0.1, rely=0.3)
        self.email_entry = tk.Entry(self.create_account)
        self.email_entry.place(relx=0.3, rely=0.3)

        balance_label = tk.Label(self.create_account, text="Opening Balance:", bg="#f0f0f0")
        balance_label.place(relx=0.1, rely=0.4)
        self.balance_entry = tk.Entry(self.create_account)
        self.balance_entry.place(relx=0.3, rely=0.4)

        pin_label = tk.Label(self.create_account, text="Pin Number:", bg="#f0f0f0")
        pin_label.place(relx=0.1, rely=0.45)
        self.pin_entry = tk.Entry(self.create_account, show="*")
        self.pin_entry.place(relx=0.3, rely=0.45)

        password_label = tk.Label(self.create_account, text="Password:", bg="#f0f0f0")
        password_label.place(relx=0.1, rely=0.5)
        self.password_entry = tk.Entry(self.create_account)
        self.password_entry.place(relx=0.3, rely=0.5)
        
        generate_btn = tk.Button(self.create_account, text="Generate", command=self.generate_password, bg="#4CAF50", fg="white", padx=1, pady=1)
        generate_btn.place(relx=0.6, rely=0.5)

        self.strength_label = tk.Label(self.create_account, text="Password Strength:", bg="#f0f0f0")
        self.strength_label.place(relx=0.1, rely=0.55)
        self.strength_bar = ttk.Progressbar(self.create_account, mode="determinate", length=200)
        self.strength_bar.place(relx=0.3, rely=0.55)

        create_btn = tk.Button(self.create_account, text="Create Account", command=self.create_account_function, bg="#4CAF50", fg="white", padx=20, pady=10)
        create_btn.place(relx=0.5, rely=0.7, anchor="center")

        back_btn = tk.Button(self.create_account, text="Back", command=self.go_back, bg="#FF5722", fg="white", padx=20, pady=10)
        back_btn.place(relx=0.3, rely=0.7, anchor="center")

        self.create_account.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_account.mainloop()

    def on_close(self):
        self.create_account.destroy()
        self.welcome_window.root.deiconify()

    def go_back(self):
        self.create_account.destroy()
        self.welcome_window.root.deiconify()

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(12))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        strength = self.calculate_strength(password)
        self.strength_bar['value'] = strength

    def calculate_strength(self, password):
        strength = 0
        if len(password) >= 8:
            strength += 20
        if any(char.isdigit() for char in password):
            strength += 20
        if any(char.isupper() for char in password):
            strength += 20
        if any(char in string.punctuation for char in password):
            strength += 20
        if len(password) >= 12:
            strength += 20
        return strength

    def create_account_function(self):
        if self.validate_entries():
            messagebox.showinfo("Success", "Account created successfully.")

    def validate_entries(self):
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        id_no = self.id_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        balance = self.balance_entry.get().strip()
        pin = self.pin_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not surname or not id_no or not phone or not email or not balance or not pin or not password:
            messagebox.showerror("Error", "All fields are required")
            return False
        return True


class LoginWindow:
    def __init__(self, welcome_window):
        self.welcome_window = welcome_window
        self.login = tk.Toplevel()
        self.login.title("Login")
        self.login.geometry("400x400")
        self.login.configure(bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        username_label = tk.Label(self.login, text="Username:", bg="#f0f0f0")
        username_label.place(relx=0.1, rely=0.3)
        self.username_entry = tk.Entry(self.login)
        self.username_entry.place(relx=0.3, rely=0.3)

        pin_label = tk.Label(self.login, text="Pin:", bg="#f0f0f0")
        pin_label.place(relx=0.1, rely=0.4)
        self.pin_entry = tk.Entry(self.login, show="*")
        self.pin_entry.place(relx=0.3, rely=0.4)

        login_btn = tk.Button(self.login, text="Login", command=self.login_function, bg="#4CAF50", fg="white", padx=20, pady=10)
        login_btn.place(relx=0.5, rely=0.7, anchor="center")

        forgot_pin_link = tk.Label(self.login, text="Forgot Pin?", fg="blue", cursor="hand2")
        forgot_pin_link.place(relx=0.6, rely=0.4)
        forgot_pin_link.bind("<Button-1>", lambda event: self.forgot_pin())

        self.new_pin_label = tk.Label(self.login, text="New Pin:", bg="#f0f0f0")
        self.new_pin_entry = tk.Entry(self.login, show="*")

        self.confirm_pin_label = tk.Label(self.login, text="Confirm Pin:", bg="#f0f0f0")
        self.confirm_pin_entry = tk.Entry(self.login, show="*")

        change_pin_btn = tk.Button(self.login, text="Change Pin", command=self.change_pin, bg="#2196F3", fg="white", padx=10, pady=5)

        back_btn = tk.Button(self.login, text="Back", command=self.go_back, bg="#FF5722", fg="white", padx=20, pady=10)
        back_btn.place(relx=0.3, rely=0.7, anchor="center")

        self.login.protocol("WM_DELETE_WINDOW", self.on_close)
        self.login.mainloop()

    def on_close(self):
        self.login.destroy()
        self.welcome_window.root.deiconify()

    def go_back(self):
        self.login.destroy()
        self.welcome_window.root.deiconify()

    def validate_entries(self):
        username = self.username_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not username or not pin:
            messagebox.showerror("Error", "Username and Pin are required")
            return False
        return True

    def forgot_pin(self):
        self.new_pin_label.place(relx=0.1, rely=0.5)
        self.new_pin_entry.place(relx=0.3, rely=0.5)
        self.confirm_pin_label.place(relx=0.1, rely=0.6)
        self.confirm_pin_entry.place(relx=0.3, rely=0.6)

        # Hide login button temporarily
        self.login_btn.place_forget()

        self.change_pin_btn.place(relx=0.5, rely=0.7, anchor="center")

    def change_pin(self):
        new_pin = self.new_pin_entry.get()
        confirm_new_pin = self.confirm_pin_entry.get()
        if new_pin == confirm_new_pin:
            self.new_pin_entry.delete(0, tk.END)
            self.confirm_pin_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Pin changed successfully.")
        else:
            messagebox.showerror("Error", "New pin and confirm pin do not match.")

    def login_function(self):
        if self.validate_entries():
            messagebox.showinfo("Success", "Login successful.")
            self.login.destroy()
            DashboardWindow(self.welcome_window)


class DashboardWindow:
    def __init__(self, welcome_window):
        self.welcome_window = welcome_window
        self.dashboard = tk.Toplevel()
        self.dashboard.title("Dashboard")
        self.dashboard.geometry("600x600")
        self.dashboard.configure(bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        view_transactions_btn = tk.Button(self.dashboard, text="View Transactions", bg="#2196F3", fg="white", padx=20, pady=10)
        view_transactions_btn.place(relx=0.5, rely=0.2, anchor="center")

        balance_inquiry_btn = tk.Button(self.dashboard, text="Balance Inquiry", bg="#2196F3", fg="white", padx=20, pady=10)
        balance_inquiry_btn.place(relx=0.5, rely=0.4, anchor="center")

        credit_debit_btn = tk.Button(self.dashboard, text="Credit/Debit Amount", bg="#2196F3", fg="white", padx=20, pady=10)
        credit_debit_btn.place(relx=0.5, rely=0.6, anchor="center")

        logout_btn = tk.Button(self.dashboard, text="Logout", command=self.logout, bg="#FF5722", fg="white", padx=20, pady=10)
        logout_btn.place(relx=0.3, rely=0.7, anchor="center")

        back_btn = tk.Button(self.dashboard, text="Back", command=self.go_back, bg="#FF5722", fg="white", padx=20, pady=10)
        back_btn.place(relx=0.5, rely=0.7, anchor="center")

        self.dashboard.protocol("WM_DELETE_WINDOW", self.on_close)
        self.dashboard.mainloop()

    def on_close(self):
        self.dashboard.destroy()
        self.welcome_window.root.deiconify()

    def go_back(self):
        self.dashboard.destroy()
        self.welcome_window.root.deiconify()

    def logout(self):
        self.dashboard.destroy()
        self.welcome_window.root.deiconify()

if __name__ == "__main__":
    WelcomeWindow()
