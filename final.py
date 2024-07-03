import re
import tkinter as tk
from tkinter import messagebox
import random
import string

class WelcomeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to SwiftBank App")
        
        self.label = tk.Label(root, text="Welcome to SwiftBank App", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Frame to hold buttons horizontally
        button_frame = tk.Frame(root)
        button_frame.pack()

        self.create_account_button = tk.Button(button_frame, text="Create Account", command=self.open_create_account)
        self.create_account_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.login_button = tk.Button(button_frame, text="Login", command=self.open_login)
        self.login_button.pack(side=tk.LEFT, padx=10, pady=10)

    def open_create_account(self):
        self.root.destroy()
        CreateAccountWindow()

    def open_login(self):
        self.root.destroy()
        LoginWindow()

        
class CreateAccountWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Create Account")
        
        self.label = tk.Label(self.root, text="Create Account", font=("Helvetica", 14))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # Username
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        # Last Name
        self.lastname_label = tk.Label(self.root, text="Last Name:")
        self.lastname_label.grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)
        self.lastname_entry = tk.Entry(self.root)
        self.lastname_entry.grid(row=2, column=1, padx=10, pady=5)

        # ID Number
        self.id_label = tk.Label(self.root, text="ID Number:")
        self.id_label.grid(row=3, column=0, sticky=tk.E, padx=10, pady=5)
        self.id_entry = tk.Entry(self.root)
        self.id_entry.grid(row=3, column=1, padx=10, pady=5)

        # Mobile/Telephone Number
        self.mobile_label = tk.Label(self.root, text="Mobile/Telephone:")
        self.mobile_label.grid(row=4, column=0, sticky=tk.E, padx=10, pady=5)
        self.mobile_entry = tk.Entry(self.root)
        self.mobile_entry.grid(row=4, column=1, padx=10, pady=5)

        # Email
        self.email_label = tk.Label(self.root, text="Email:")
        self.email_label.grid(row=5, column=0, sticky=tk.E, padx=10, pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=5, column=1, padx=10, pady=5)

        # Opening Balance
        self.opening_balance_label = tk.Label(self.root, text="Opening Balance:")
        self.opening_balance_label.grid(row=6, column=0, sticky=tk.E, padx=10, pady=5)
        self.opening_balance_entry = tk.Entry(self.root)
        self.opening_balance_entry.grid(row=6, column=1, padx=10, pady=5)

        # PIN
        self.pin_label = tk.Label(self.root, text="PIN:")
        self.pin_label.grid(row=7, column=0, sticky=tk.E, padx=10, pady=5)
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.grid(row=7, column=1, padx=10, pady=5)

        # Frame to hold buttons horizontally
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)

        self.create_account_button = tk.Button(button_frame, text="Create Account", command=self.create_account)
        self.create_account_button.pack(side=tk.LEFT, padx=5)

        self.back_button = tk.Button(button_frame, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=5)

        self.root.mainloop()

    def create_account(self):
        username = self.username_entry.get().strip()
        lastname = self.lastname_entry.get().strip()
        id_number = self.id_entry.get().strip()
        mobile_number = self.mobile_entry.get().strip()
        email = self.email_entry.get().strip()
        opening_balance = self.opening_balance_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if username and lastname and id_number and mobile_number and email and opening_balance and pin:
            try:
                opening_balance = float(opening_balance)
                if opening_balance >= 0:
                    # Save account details (for simplicity, we'll keep it in memory here)
                    messagebox.showinfo("Account Created", "Account created successfully!")
                    self.root.destroy()
                    WelcomeWindow(tk.Tk())
                else:
                    messagebox.showerror("Error", "Opening balance cannot be negative.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input for opening balance.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def go_back(self):
        self.root.destroy()
        WelcomeWindow(tk.Tk())
# Example usage
if __name__ == "__main__":
    CreateAccountWindow()

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")

        self.label = tk.Label(self.root, text="Login", font=("Helvetica", 14))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        self.pin_label = tk.Label(self.root, text="PIN:")
        self.pin_label.grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.grid(row=2, column=1, padx=10, pady=5)

        # Frame to hold buttons horizontally
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.login_button = tk.Button(button_frame, text="Login", command=self.login)
        self.login_button.pack(side=tk.LEFT, padx=5)

        self.back_button = tk.Button(button_frame, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=5)

        self.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        pin = self.pin_entry.get()

        # Simulating a fixed PIN for demonstration
        if username == "user" and pin == "1234":
            self.root.destroy()
            DashboardWindow(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or PIN.")

    def go_back(self):
        self.root.destroy()
        WelcomeWindow(tk.Tk())
class DashboardWindow:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title("Dashboard")

        self.username = username
        self.balance = 1000.0  # Initialize balance (for simplicity)

        self.balance_label = tk.Label(self.root, text=f"Welcome, {self.username} | Balance: R{self.balance}", font=("Helvetica", 12))
        self.balance_label.pack(pady=20)

        # Frame to hold buttons horizontally
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.withdraw_button = tk.Button(button_frame, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack(side=tk.LEFT, padx=5)

        self.deposit_button = tk.Button(button_frame, text="Deposit", command=self.deposit)
        self.deposit_button.pack(side=tk.LEFT, padx=5)

        self.check_balance_button = tk.Button(button_frame, text="Check Balance", command=self.check_balance)
        self.check_balance_button.pack(side=tk.LEFT, padx=5)

        self.logout_button = tk.Button(button_frame, text="Logout", command=self.logout)
        self.logout_button.pack(side=tk.LEFT, padx=5)

        self.back_button = tk.Button(self.root, text="Back", command=self.go_back)
        self.back_button.pack(pady=10)

        self.root.mainloop()

    def withdraw(self):
        amount = float(messagebox.askstring("Withdraw", "Enter amount to withdraw:"))
        if amount <= self.balance:
            self.balance -= amount
            messagebox.showinfo("Withdrawal", f"${amount} withdrawn successfully.")
            self.update_balance_label()
        else:
            messagebox.showerror("Error", "Insufficient funds.")

    def deposit(self):
        amount = float(messagebox.askstring("Deposit", "Enter amount to deposit:"))
        self.balance += amount
        messagebox.showinfo("Deposit", f"${amount} deposited successfully.")
        self.update_balance_label()

    def check_balance(self):
        messagebox.showinfo("Balance", f"Current Balance: ${self.balance}")

    def update_balance_label(self):
        self.balance_label.config(text=f"Welcome, {self.username} | Balance: ${self.balance}")

    def logout(self):
        self.root.destroy()
        WelcomeWindow(tk.Tk())

    def go_back(self):
        self.root.destroy()
        LoginWindow()

if __name__ == "__main__":
    root = tk.Tk()
    WelcomeWindow(root)
    root.mainloop()
