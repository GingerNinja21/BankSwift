import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog,filedialog
import datetime
import pandas as pd
from file import DataValidation, account_creation
from PIL import Image, ImageTk

class BankingApplicationGUI(tk.Toplevel):
    def __init__(self, parent,current_user_name,id_no,banks_file,transactions_log):
        super().__init__(parent)
        self.parent= parent
        self.title("Banking GUI")
    
        self.current_user = current_user_name
        self.id_no= id_no
        self.accounts_file = "accounts.csv"
        self.banks_file = banks_file
        self.transactions_log = transactions_log
        self.display_name = self.current_user.capitalize()
        
        self.account_no=""
        
                
        
        
        self.account_validator()
        window_width = 800
        window_height = 600

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.resizable(False, False)
        self.grab_set()

        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        
        self.background_image = Image.open("background.png")
        self.logo_image = Image.open("logo_transparent.png")
    
        
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((2000, 2000)))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image.resize((100,100)))

        

        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)
        self.canvas.create_image(750, 550, image=self.logo_photo, anchor=tk.SE)

        self.protocol("WM_DELETE_WINDOW", self.go_back)

        self.create_widgets()

    def account_validator(self):
        valid_acc= False
        with open("accounts.csv", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) > 6 and self.current_user == parts[1]:
                    self.account_no = parts[3]
                    valid_acc= True
                    print(self.account_no)
                    return valid_acc
            
            messagebox.showerror("Error!","Something went wrong while initiating account numbers.\nContact Support!")
        

    def create_widgets(self):

        login_banner_label=tk.Label(self.canvas, text=f"Welcome\n{self.display_name}",font=("Times New Roman", 30,"bold") ,fg="#a1c8ff" , bg="#0a1627")
        login_banner_label.place(relx=0.5, rely=0.1 ,anchor="center", width=790)

        self.view_balance_button = tk.Button(self.canvas, text="View Balance", command=self.view_balance ,font=("Times New Roman", 17,"bold"),bg="#090f16", fg="#FFFFFF")
        self.view_balance_button.place(relx=0.3, rely=0.3, anchor="center", width=150 , height=100)

        self.withdraw_button = tk.Button(self.canvas, text="Withdraw", command=self.withdraw,font=("Times New Roman", 17,"bold"),bg="#090f16", fg="#FFFFFF")
        self.withdraw_button.place(relx=0.65, rely=0.3, anchor="center", width=150 , height=100)

        self.transfer_button = tk.Button(self.canvas, text="Transfer", command=self.transfer,font=("Times New Roman", 17,"bold"), bg="#090f16", fg="#FFFFFF")
        self.transfer_button.place(relx=0.3, rely=0.6, anchor="center", width=150 , height=100)

        self.view_transactions_button = tk.Button(self.canvas, text="View\nTransactions", command=self.view_transactions ,font=("Times New Roman", 15,"bold"),bg="#090f16", fg="#FFFFFF")
        self.view_transactions_button.place(relx=0.65, rely=0.6, anchor="center", width=150 , height=100)
        
        self.back_btn= tk.Button(self.canvas, text="Close", command=self.go_back,font=("Times New Roman", 17,"bold"),bg="#230e11", fg="#FFFFFF")
        self.back_btn.place(relx=0.47, rely=0.8, anchor="center", width=100 , height=60)
    
    def go_back(self):
        self.destroy()
        self.parent.deiconify()
     
        

    def view_balance(self):
        balance = self.get_balance_from_csv(self.account_no)
        if balance is not None:
            messagebox.showinfo("Balance", f"Your balance is R{balance:.2f}",parent=self.canvas)
        else:
            messagebox.showerror("Error", "Failed to retrieve balance.",parent=self.canvas)
 

    def get_balance_from_csv(self,acc_no):
        global transfer_recipient_user
        try:
            df = pd.read_csv('accounts.csv')
            account_no=int(acc_no)
            if account_no in df['account_no'].values:
                row = df[df['account_no'] == account_no]
                return row['balance'].values[0]
            else:
                messagebox.showerror("Error", f"Account '{acc_no}' not found.",parent=self.canvas)
        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts file not found.",parent=self.canvas)
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving balance: {str(e)}",parent=self.canvas)
            return None

    def get_account_no(self, account_name):
        try:
            df = pd.read_csv(self.accounts_file)
            account = df[df['name'].str.lower() == account_name.lower()]
            if not account.empty:
                return account['account_no'].values[0]
            else:
                messagebox.showerror("Error", f"Account  '{account_name}' not found.",parent=self.canvas)
                return None
        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts file not found.",parent=self.canvas)
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving account number: {str(e)}",parent=self.canvas)
            return None
        
    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:",parent=self.canvas)
        try:
            if amount is None or amount <= 0:
                messagebox.showerror("Error", "Invalid amount.",parent=self.canvas)
                return

            current_balance = int(self.get_balance_from_csv(self.account_no))
            if current_balance is None:
                return  

            if amount > current_balance:
                messagebox.showerror("Error", "Insufficient funds.",parent=self.canvas)
                return

            self.update_balance(-amount,self.account_no)
            self.write_transaction("Withdraw", amount)
            messagebox.showinfo("Withdraw", f"R{amount:.2f} successfully withdrawn.",parent=self.canvas)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            

    def transfer(self):
        valid_account=False
        global transfer_recipient_user
        transfer_recipient_user = simpledialog.askstring("Transfer", "Enter recipient account name:")
        recipient_account_no = simpledialog.askstring("Transfer", "Enter recipient account number:")
        amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")

        try:
            if not transfer_recipient_user or not recipient_account_no or not amount or amount <= 0:
                messagebox.showerror("Error", "Invalid input.",parent=self.canvas)
                return
            
            with open("accounts.csv", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) > 6 and transfer_recipient_user == parts[1] and recipient_account_no == parts[3]:
                        valid_account = True
                    
                        

            if valid_account:            
                current_balance = self.get_balance_from_csv(self.account_no)
                if current_balance is None:
                    return

                if amount > current_balance:
                    messagebox.showerror("Error", "Insufficient funds.",parent=self.canvas)
                    return 
                
                if self.update_balance(-amount,self.account_no):
                    self.write_transaction("Transfer", amount , transfer_recipient_user.lower(), recipient_account_no)
                    self.update_balance(amount,recipient_account_no)
                    messagebox.showinfo("Transfer", f"R{amount:.2f} successfully transferred to {transfer_recipient_user}.", parent=self.canvas)
                    return
            else:
                messagebox.showerror("Error","The account number provided does not match any account in our database!\nPlease try again.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.",parent=self.canvas)

    def view_transactions(self):
        try:
            account_no =self.account_no
            transactions_window = tk.Toplevel(self)
            # transactions_window_canvas = tk.Canvas(self.root, width=800, height=600)
            # transactions_window_canvas.pack(fill="both", expand=True)
            transactions_window.title("Transaction History")
            # transactions_window.geometry("800x600")
            window_width = 900
            window_height = 700

            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            center_x = int(screen_width / 2 - window_width / 2)
            center_y = int(screen_height / 2 - window_height / 2)

            transactions_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

            transactions_window.resizable(False, False)
            transactions_window.grab_set()

            transactions_window_canvas = tk.Canvas(self, width=800, height=600)
            transactions_window_canvas.pack(fill="both", expand=True)
            
            background_image = Image.open("background.png")
            logo_image = Image.open("logo_transparent.png")
        
            
            apply_background_photo = ImageTk.PhotoImage(background_image.resize((2000, 2000)))
            apply_logo_photo = ImageTk.PhotoImage(logo_image.resize((100,100)))

            

            transactions_window_canvas.create_image(0, 0, image=apply_background_photo, anchor=tk.NW)
            transactions_window_canvas.create_image(750, 550, image=apply_logo_photo, anchor=tk.SE)

            transactions_text = scrolledtext.ScrolledText(transactions_window, width=100, height=30)
            transactions_text.pack(padx=20, pady=20)

            with open(self.transactions_log, "r") as file:
                transactions = file.readlines()

            formatted_transactions = []
            for transaction in transactions:
                if account_no in transaction:
                    formatted_transactions.append(transaction.strip() + "\n")

            if formatted_transactions:
                transactions_text.insert(tk.END, "".join(formatted_transactions))
            else:
                 transactions_text.insert(tk.END, "No transactions found for account number " + account_no)
            # transactions_text.insert(tk.END, "".join(formatted_transactions))
            transactions_text.configure(state="disabled")  # widget uneditable

        except FileNotFoundError:
            messagebox.showerror("Error", "Transaction log file not found.",parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view transactions: {str(e)}",parent=self.canvas)

    # def get_account_type(self, account_name):
    #     try:
    #         df = pd.read_csv(self.accounts_file)
    #         account = df[df['name'].str.lower() == account_name.lower() and df["id_no"]]
    #         if not account.empty:
    #             return account['account_type'].values[0]
    #         else:
    #             messagebox.showinfo("New Account", f"Account '{account_name}' not found. Creating new account...",parent=self.canvas)
    #             self.create_new_account(account_name)
    #             return ""  # Handle new account creation
    #     except FileNotFoundError:
    #         messagebox.showerror("Error", "Accounts file not found.",parent=self.canvas)
    #         return 

    # def create_new_account(self, account_name):
    #     new_account_id = simpledialog.askstring("New Account", "Enter your ID number:")
    #     acc_type = simpledialog.askstring("New Account", "Enter account type (Savings/Cheque):")

    #     creation = account_creation(account_name, "unknown", new_account_id, acc_type)
    #     if creation.get_error_mnssage():
    #         messagebox.showerror("Error", creation.get_error_message(), parent=self.canvas)
    #     else:
    #         new_account_no = creation.acc_no_generator()

    #         new_account_data = {
    #             'uid': [0],  # Assign UID appropriately
    #             'name': [account_name],
    #             'surname': ['unknown'],
    #             'account_no': [new_account_no],
    #             'balance': [100],  # Initial balance
    #             'account_type': [acc_type],
    #             'id_number': [new_account_id],
    #             'linked_accounts': ['']
    #         }

    #         new_account_data_df = pd.DataFrame(new_account_data)

    #         try:
    #             df = pd.read_csv(self.accounts_file)
    #             df = pd.concat([df, new_account_data_df], ignore_index=True)
    #             df.to_csv(self.accounts_file, index=False)
    #             messagebox.showinfo("New Account", f"New account created for {account_name} with account number {new_account_no}.",parent=self.canvas)
    #         except FileNotFoundError:
    #             messagebox.showerror("Error", "Accounts file not found.",parent=self.canvas)


    def write_transaction(self, transaction_type, amount, to_account=None, to_account_no=None):
        try:
            transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            from_account_name = self.current_user
            from_account_no = self.account_no

            if transaction_type == "Transfer" and to_account and to_account_no:
                transaction_details = f" {transaction_time} - {transaction_type}: R{amount:.2f} - From: {from_account_name} ({from_account_no}) to {to_account} ({to_account_no})\n"
            else:
                transaction_details = f" {transaction_time} - {transaction_type}: R{amount:.2f} - From: {from_account_name} ({from_account_no})\n"

            with open(self.transactions_log, "a") as file:
                file.write(transaction_details)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to write transaction: {str(e)}",parent=self.canvas)

    def update_balance(self, amount,acc_no):
        try:
            account_no= int(acc_no)
           
            df = pd.read_csv(self.accounts_file)
            account = df[df["account_no"] == account_no]
            
            if not account.empty:
                new_balance = account['balance'].values[0] + amount
                print("account found " ,account_no)
                df.loc[df['account_no'] == account_no ,'balance'] = new_balance
                df.to_csv(self.accounts_file, index=False)
                return True
            else:
                messagebox.showerror("Error", f"Account '{acc_no}' not found.",parent=self.canvas)
                return False
        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts file not found.",parent=self.canvas)
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update balance: {str(e)}",parent=self.canvas)
            return False

if __name__ == "__main__":
    window= tk.Tk()
    x= BankingApplicationGUI(window,"abigail","0210085197080","banks.csv","transactionslog.txt",)
    x.mainloop()
 