import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
#from PIL import Image, ImageTk

#BG_COLOR = "#ADD8E6"

class WelcomeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to BankSwift App")
        self.style = ttk.Style(self.root.tk)
        self.style.theme_use('clam')

        #canvas
        self.canvas = Tk.Canvas(root, width=500, height=250)
        self.canvas.pack()
   
        #self.root.configure(bg=BG_COLOR)
   
        self.label = Tk.Label(root, text="Welcome to BankSwift", font=("Roboto", 16))
        self.label.pack(pady=20)

        # Frame to hold buttons horizontally
        button_frame = Tk.Frame(root)
        button_frame.pack()

        self.create_account_button = Tk.Button(button_frame, text="Create Account", command=self.open_create_account)
        self.create_account_button.pack(side=Tk.LEFT, padx=10, pady=10)

        self.login_button = Tk.Button(button_frame, text="Login", command=self.open_login)
        self.login_button.pack(side=Tk.LEFT, padx=10, pady=10)

    def open_create_account(self):
        self.root.destroy()
        CreateAccountWindow()

    def open_login(self):
        self.root.destroy()
        LoginWindow()

class CreateAccountWindow:
    def __init__(self):
        self.root = Tk.Tk()
        self.root.title("Create Account")

        self.canvas = Tk.Canvas(root, width=500, height=250)
        self.canvas.pack()
        
        self.label = Tk.Label(self.root, text="Create Account", font=("Roboto", 14))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.username_label = Tk.Label(self.root, text="Username: ")
        self.username_label.grid(row=1, column=0, sticky=Tk.E, padx=10, pady=5)
        self.username_entry = Tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        self.opening_balance_label = Tk.Label(self.root, text="Opening Balance:")
        self.opening_balance_label.grid(row=2, column=0, sticky=Tk.E, padx=10, pady=5)
        self.opening_balance_entry = Tk.Entry(self.root)
        self.opening_balance_entry.grid(row=2, column=1, padx=10, pady=5)

        self.pin_label = Tk.Label(self.root, text="PIN:")
        self.pin_label.grid(row=3, column=0, sticky=Tk.E, padx=10, pady=5)
        self.pin_entry = Tk.Entry(self.root, show="*")
        self.pin_entry.grid(row=3, column=1, padx=10, pady=5)

        # Frame to hold buttons horizontally
        button_frame = Tk.Frame(self.root)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        self.create_account_button = Tk.Button(button_frame, text="Create Account", command=self.create_account)
        self.create_account_button.pack(side=Tk.LEFT, padx=5)

        self.back_button = Tk.Button(button_frame, text="Back", command=self.go_back)
        self.back_button.pack(side=Tk.LEFT, padx=5)

        self.root.mainloop()

    def create_account(self):
        username = self.username_entry.get()
        opening_balance = self.opening_balance_entry.get()
        pin = self.pin_entry.get()

        if username and opening_balance and pin:
            try:
                opening_balance = float(opening_balance)
                if opening_balance >= 0:
                    # Save account details (for simplicity, we'll keep it in memory here)
                    messagebox.showinfo("Account Created", "Account created successfully!")
                    self.root.destroy()
                    WelcomeWindow(Tk.Tk())
                else:
                    messagebox.showerror("Error", "Opening balance cannot be negative.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input for opening balance.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def go_back(self):
        self.root.destroy()
        WelcomeWindow(Tk.Tk())


class LoginWindow:
    def __init__(self):
        self.root = Tk.Tk()
        self.root.title("Login")

        self.canvas = Tk.Canvas(root, width=500, height=250)
        self.canvas.pack()

        self.label = Tk.Label(self.root, text="Login", font=("Roboto", 14))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.username_label = Tk.Label(self.root, text="Username:")
        self.username_label.grid(row=1, column=0, sticky=Tk.E, padx=10, pady=5)
        self.username_entry = Tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        self.pin_label = Tk.Label(self.root, text="PIN:")
        self.pin_label.grid(row=2, column=0, sticky=Tk.E, padx=10, pady=5)
        self.pin_entry = Tk.Entry(self.root, show="*")
        self.pin_entry.grid(row=2, column=1, padx=10, pady=5)

        # Frame to hold buttons horizontally
        button_frame = Tk.Frame(self.root)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.login_button = Tk.Button(button_frame, text="Login", command=self.login)
        self.login_button.pack(side=Tk.LEFT, padx=5)

        self.back_button = Tk.Button(button_frame, text="Back", command=self.go_back)
        self.back_button.pack(side=Tk.LEFT, padx=5)

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
        WelcomeWindow(Tk.Tk())

class DashboardWindow:
    def __init__(self, username):
        self.root = Tk.Tk()
        self.root.title("Dashboard")

        self.username = username
        self.balance = 1000.0  # Initialize balance (for simplicity)

        self.balance_label = Tk.Label(self.root, text=f"Welcome, {self.username} | Balance: R{self.balance}", font=("Roboto", 12))
        self.balance_label.pack(pady=20)

        # Frame to hold buttons horizontally
        button_frame = Tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.withdraw_button = Tk.Button(button_frame, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack(side=Tk.LEFT, padx=5)

        self.deposit_button = Tk.Button(button_frame, text="Deposit", command=self.deposit)
        self.deposit_button.pack(side=Tk.LEFT, padx=5)

        self.check_balance_button = Tk.Button(button_frame, text="Check Balance", command=self.check_balance)
        self.check_balance_button.pack(side=Tk.LEFT, padx=5)

        self.logout_button = Tk.Button(button_frame, text="Logout", command=self.logout)
        self.logout_button.pack(side=Tk.LEFT, padx=5)

        self.back_button = Tk.Button(self.root, text="Back", command=self.go_back)
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
        WelcomeWindow(Tk.Tk())

    def go_back(self):
        self.root.destroy()
        LoginWindow()

if __name__ == "__main__":
    root = Tk.Tk()

WelcomeWindow(root)
root.mainloop()
