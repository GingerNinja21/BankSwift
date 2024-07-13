import csv
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import datetime
import pandas as pd
from file import DataValidation, account_creation


class BankingApplicationGUI(tk.Tk):
    def __init__(self, recipient_name, accounts_file, banks_file, transactions_log,id_no):
        super().__init__()
        self.recipient_name = recipient_name
        self.id_no= id_no
        self.accounts_file = "accounts.csv"
        self.banks_file = banks_file
        self.transactions_log = transactions_log
        # self.account_type = self.get_account_type(recipient_name)

        self.title("BankSwift")
        self.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.view_balance_button = tk.Button(self, text="View Balance", command=self.view_balance)
        self.view_balance_button.pack(pady=10)

        self.withdraw_button = tk.Button(self, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack(pady=10)

        self.transfer_button = tk.Button(self, text="Transfer", command=self.transfer)
        self.transfer_button.pack(pady=10)

        self.view_transactions_button = tk.Button(self, text="View Transactions", command=self.view_transactions)
        self.view_transactions_button.pack(pady=10)

    def view_balance(self):
        recipient_name = self.entry_recipient_name.get()
        id_no = self.entry_id_no.get()

        if not recipient_name or not id_no:
            messagebox.showerror("Error", "Please enter recipient name and ID number.")
            return

        validator = DataValidation(recipient_name=recipient_name, id_no=id_no)
        balance = validator.get_balance_from_csv()

        self.label_balance.config(text=f"Balance: R{balance:.2f}")
        messagebox.showinfo("Balance", f"Your balance is R{balance:.2f}")

    def get_balance_from_csv(self):
        try:
            with open("accounts.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    stored_id = row["id_number"].strip().lower()
                    stored_name = row["name"].strip().lower()
                    stored_surname = row["surname"].strip().lower()
                    stored_balance = float(row["balance"]) 
                    if self.id_no == stored_id and self.recipient_name == stored_name and self.recipient_surname == stored_surname:
                        return stored_balance

            messagebox.showerror("Error", "Account not found.")
            return 0.0

        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts file not found.")
            return 0.0

        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving balance: {str(e)}")
            return 0.0

    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        try:
            if amount is None or amount <= 0:
                messagebox.showerror("Error", "Invalid amount.")
                return

            if self.update_balance(-amount):
                self.write_transaction("Withdraw", amount)
                messagebox.showinfo("Withdraw", f"R{amount:.2f} successfully withdrawn.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            
    def transfer(self):
        recipient_name = simpledialog.askstring("Transfer", "Enter recipient account name:")
        amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")

        try:
            if not recipient_name or not amount or amount <= 0:
                messagebox.showerror("Error", "Invalid input.")
                return

            if self.update_balance(-amount):
                self.write_transaction("Transfer", amount, recipient_name)
                messagebox.showinfo("Transfer", f"R{amount:.2f} successfully transferred to {recipient_name}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")

    def view_transactions(self):
        try:
            transactions_window = tk.Toplevel(self)
            transactions_window.title("Transaction History")
            transactions_window.geometry("600x400")

            transactions_text = scrolledtext.ScrolledText(transactions_window, width=80, height=20)
            transactions_text.pack(padx=20, pady=20)

            with open(self.transactions_log, "r") as file:
                transactions = file.read()
                transactions_text.insert(tk.END, transactions)

        except FileNotFoundError:
            messagebox.showerror("Error", "Transaction log file not found.")

    def get_account_type(self, account_name):
        try:
            df = pd.read_csv(self.accounts_file)
            account = df[df['name'].str.lower() == account_name.lower() and df["id_no"]]
            if not account.empty:
                return account['account_type'].values[0]
            else:
                messagebox.showinfo("New Account", f"Account '{account_name}' not found. Creating new account...")
                self.create_new_account(account_name)
                return ""  # Handle new account creation
        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts file not found.")
            return ""

    def create_new_account(self, account_name):
        new_account_id = simpledialog.askstring("New Account", "Enter your ID number:")
        acc_type = simpledialog.askstring("New Account", "Enter account type (Savings/Cheque):")

        creation = account_creation(account_name, "unknown", new_account_id, acc_type)
        if creation.get_error_message():
            messagebox.showerror("Error", creation.get_error_message())
        else:
            new_account_no = creation.acc_no_generator()

            new_account_data = {
                'uid': [0],  # Assign UID appropriately
                'name': [account_name],
                'surname': ['unknown'],
                'account_no': [new_account_no],
                'balance': [100],  # Initial balance
                'account_type': [acc_type],
                'id_number': [new_account_id],
                'linked_accounts': ['']
            }

            new_account_data_df = pd.DataFrame(new_account_data)

            try:
                df = pd.read_csv(self.accounts_file)
                df = pd.concat([df, new_account_data_df], ignore_index=True)
                df.to_csv(self.accounts_file, index=False)
                messagebox.showinfo("New Account", f"New account created for {account_name} with account number {new_account_no}.")
            except FileNotFoundError:
                messagebox.showerror("Error", "Accounts file not found.")

    def write_transaction(self, transaction_type, amount, to_account=None):
        try:
            transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            from_account_name = self.recipient_name
            transaction_details = f"{transaction_time} - {transaction_type}: R{amount:.2f} - From: {from_account_name}\n"

            with open(self.transactions_log, "a") as file:
                file.write(transaction_details)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to write transaction: {str(e)}")

    def update_balance(self, amount):
        try:
            df = pd.read_csv(self.accounts_file)
            mask = df['name'].str.lower() == self.recipient_name.lower()
            if mask():
                df.loc[mask, 'balance'] += amount
                df.to_csv(self.accounts_file, index=False)
            else:
                messagebox.showerror("Error", f"Account '{self.recipient_name}' not found.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts file not found.")

# if __name__ == "__main__":
#     # recipient_name = simpledialog.askstring("Login", "Enter your account name:")
#     # app = BankingApplicationGUI(
#         recipient_name,
#         accounts_file="accounts.csv",
#         banks_file="banks.csv",
#         transactions_log="transactionslog.txt"
#     )
    # app.mainloop()
# 