import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog,filedialog
import datetime
import pandas as pd
from file import DataValidation, account_creation
from PIL import Image, ImageTk

class BankingApplicationGUI(tk.Toplevel):
    def __init__(self, parent,current_user_name,id_no,banks_file,transactions_log,account_no, multi_acc = False):
        super().__init__()
        self.parent= parent
        self.LoginMenu=self
        self.LoginMenu.title("Banking GUI")

    
        self.current_user = current_user_name
        self.multi_acc = multi_acc
        self.id_no= id_no
        self.accounts_file = "accounts.csv"
        self.banks_file = banks_file
        self.transactions_log = transactions_log
        self.display_name = self.current_user.capitalize()
        
        self.account_no=account_no
        self.user_surname=""
        self.acc_type=""
        
        
        self.account_validator()
       
        window_width = 800
        window_height = 600

        screen_width = self.LoginMenu.winfo_screenwidth()
        screen_height = self.LoginMenu.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.LoginMenu.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.LoginMenu.resizable(False, False)


        self.LoginMenu_canvas = tk.Canvas(self.LoginMenu, width=800, height=600)
        self.LoginMenu_canvas.pack(fill="both", expand=True)
        
        self.LoginMenu_background_image = Image.open("background.png")
        self.LoginMenu_logo_image = Image.open("logo_transparent.png")
    
        
        self.LoginMenu_background_photo = ImageTk.PhotoImage(self.LoginMenu_background_image.resize((2000, 2000)))
        self.LoginMenu_logo_photo = ImageTk.PhotoImage(self.LoginMenu_logo_image.resize((100,100)))

        

        self.LoginMenu_canvas.create_image(0, 0, image=self.LoginMenu_background_photo, anchor=tk.NW)
        self.LoginMenu_canvas.create_image(750, 550, image=self.LoginMenu_logo_photo, anchor=tk.SE)

        self.LoginMenu.protocol("WM_DELETE_WINDOW", self.go_back)
        

        self.create_widgets()
        
    def account_validator(self):
        valid_acc= False
        with open("accounts.csv", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) > 6 and self.account_no == parts[3]:
                    self.user_surname= parts[2]
                    self.acc_type=parts[5]
                    valid_acc= True
                    print(self.account_no)
                    return valid_acc
            
            messagebox.showerror("Error!","Something went wrong while initiating account numbers.\nContact Support!")
        

    def create_widgets(self):

        self.view_balance_loginGUI()
        login_banner_label=tk.Label(self.LoginMenu_canvas, text=f"{self.display_name.capitalize()} {self.user_surname.capitalize()}",font=("Times New Roman", 30,"bold") ,fg="#a1c8ff" , bg="#090f16")
        login_banner_label.place(relx=0.5, rely=0.095 ,anchor="center", width=790)
        login_banner2_label=tk.Label(self.LoginMenu_canvas, text=f"{self.acc_type.capitalize()} : {self.account_no}",font=("Times New Roman", 15,"bold") ,fg="#FFFFFF" , bg="#0a1627")
        login_banner2_label.place(relx=0.5, rely=0.16 ,anchor="center", width=790)


        self.withdraw_button = tk.Button(self.LoginMenu_canvas, text="Withdraw", command=self.withdraw_GUI , font=("Times New Roman", 17,"bold"),bg="#090f16", fg="#FFFFFF")
        self.withdraw_button.place(relx=0.7, rely=0.5, anchor="center", width=150 , height=100)

        self.transfer_button = tk.Button(self.LoginMenu_canvas, text="Transfer", command=self.transfer_GUI,font=("Times New Roman", 17,"bold"), bg="#090f16", fg="#FFFFFF")
        self.transfer_button.place(relx=0.3, rely=0.5, anchor="center", width=150 , height=100)

        self.view_transactions_button = tk.Button(self.LoginMenu_canvas, text="View\nTransactions", command=self.view_transactions ,font=("Times New Roman", 15,"bold"),bg="#090f16", fg="#FFFFFF")
        self.view_transactions_button.place(relx=0.5, rely=0.6, anchor="center", width=150 , height=100)
        
        self.back_btn= tk.Button(self.LoginMenu_canvas, text="Close", command=self.go_back,font=("Times New Roman", 17,"bold"),bg="#230e11", fg="#FFFFFF")
        self.back_btn.place(relx=0.5, rely=0.8, anchor="center", width=100 , height=60)
    
    def go_back(self):
        self.destroy()
        if self.multi_acc:
            self.parent.deiconify()
        else:
            self.parent.deiconify()
        

    def view_balance_loginGUI(self):
        balance = self.get_balance_from_csv(self.account_no)
        if balance is not None:
            self.view_balance_button = tk.Button(self.LoginMenu_canvas, state="disabled",font=("Times New Roman", 25,"bold"),bg="#0a1627", fg="#FFFFFF")
            self.view_balance_button.place(relx=0.5, rely=0.3, anchor="center", width=600 , height=100)

            login_banner_label=tk.Label(self.LoginMenu_canvas, text=f"Balance:",font=("Times New Roman", 25,"bold"),bg="#0a1627", fg="#2e6b7f")
            login_banner_label.place(relx=0.5, rely=0.25 ,anchor="center", width=300 ,height=30)

            login_banner_label2=tk.Label(self.LoginMenu_canvas, text=f"R{balance}",font=("Times New Roman", 25,"bold"),bg="#0a1627", fg="#789aa2")
            login_banner_label2.place(relx=0.5, rely=0.32 ,anchor="center", width=150, height=30)


        else:
            messagebox.showerror("Error", "Failed to retrieve balance.",parent=self.LoginMenu_canvas)

    
    def view_balance_withdrawGUI(self):
        balance = self.get_balance_from_csv(self.account_no)
        self.view_balance_button = tk.Button(self.withdraw_canvas, state="disabled",font=("Times New Roman", 25,"bold"),bg="#0a1627")
        self.view_balance_button.place(relx=0.5, rely=0.1, anchor="center", width=400 , height=100)

        self.withdraw_banner_label=tk.Label(self.withdraw_canvas, text="Current Balance:",font=("Times New Roman", 25,"bold"),bg="#0a1627", fg="#2e6b7f")
        self.withdraw_banner_label.place(relx=0.5, rely=0.075 ,anchor="center", width=300)

        self.withdraw_banner2_label=tk.Label(self.withdraw_canvas, text=f"R{balance}",font=("Times New Roman", 20,"bold"),bg="#0a1627", fg="#789aa2")
        self.withdraw_banner2_label.place(relx=0.5, rely=0.13 ,anchor="center", width=150 ,height=30)
        

 

    def get_balance_from_csv(self,acc_no):
        try:
            df = pd.read_csv('accounts.csv')
            account_no=int(acc_no)
            if account_no in df['account_no'].values:
                row = df[df['account_no'] == account_no]
                return row['balance'].values[0]
            else:
                messagebox.showerror("Error", f"Account '{acc_no}' not found.",parent=self.LoginMenu_canvas)
        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts file not found.",parent=self.LoginMenu_canvas)
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving balance: {str(e)}",parent=self.LoginMenu_canvas)
            return None

    def get_account_no(self, account_name):
        try:
            df = pd.read_csv(self.accounts_file)
            account = df[df['name'].str.lower() == account_name.lower()]
            if not account.empty:
                return account['account_no'].values[0]
            else:
                messagebox.showerror("Error", f"Account  '{account_name}' not found.",parent=self.LoginMenu_canvas)
                return None
        except FileNotFoundError:
            messagebox.showerror("Error", "Accounts file not found.",parent=self.LoginMenu_canvas)
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving account number: {str(e)}",parent=self.LoginMenu_canvas)
            return None
        
    def withdraw_GUI(self):
        try:
            self.LoginMenu.iconify()
            account_no =self.account_no
            self.withdraw_window = tk.Toplevel()
            self.withdraw_window.title("Withdraw")
            self.withdraw_window.resizable(False, False)
            window_width = 500
            window_height = 600

            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            center_x = int(screen_width / 2 - window_width / 2)
            center_y = int(screen_height / 2 - window_height / 2)

            self.withdraw_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

            self.withdraw_canvas = tk.Canvas(self.withdraw_window, width=800, height=600)
            self.withdraw_canvas.pack(fill="both", expand=True)
            
            self.withdraw_background_image = Image.open("background.png")
            self.withdraw_logo_image = Image.open("logo_transparent.png")
           
    
            self.withdraw_background_photo = ImageTk.PhotoImage(self.withdraw_background_image.resize((2000, 2000)))
            self.withdraw_logo_photo = ImageTk.PhotoImage(self.withdraw_logo_image.resize((100,100)))

            self.withdraw_back_button = tk.Button(self.withdraw_canvas, text="Back", command = self.on_withdraw_close ,font =("Times New Roman", 17,"bold"),bg="#230e11", fg="#FFFFFF")
            self.withdraw_back_button.place(relx=0.5, rely=0.7, anchor="center", width=80 , height=50)

            self.withdraw_confirm_button = tk.Button(self.withdraw_canvas, text="Withdraw", command = self.withdraw_function ,font =("Times New Roman", 15,"bold"),bg="#8a9099", fg="#FFFFFF")
            self.withdraw_confirm_button.place(relx=0.5, rely=0.6, anchor="center", width=100 , height=50)


            self.withdraw_canvas.create_image(0, 0, image=self.withdraw_background_photo, anchor=tk.NW)
            self.withdraw_canvas.create_image(470,570, image=self.withdraw_logo_photo, anchor=tk.SE)
            
            self.withdraw_amount_background= tk.Button(self.withdraw_canvas, state="disabled",font=("Times New Roman", 25,"bold"),bg="#090f16", fg="#FFFFFF")
            self.withdraw_amount_background.place(relx=0.5, rely=0.4, anchor="center", width=250 , height=50)

            self.withdraw_amount_label = tk.Label(self.withdraw_canvas, text="Withdraw Amount:", font=("Times New Roman", 17, "bold") , fg="#789aa2" , bg="#090f16")
            self.withdraw_amount_label.place(relx=0.5, rely=0.4,anchor="center")
            self.withdraw_amount_entry = tk.Entry(self.withdraw_canvas,font=("Times New Roman", 30))
            self.withdraw_amount_entry.configure(bg="#2c3747",fg="#FFFFFF", justify="center")
            self.withdraw_amount_entry.place(relx=0.5, rely=0.5 , anchor="center" , width=200 , height=50)

            
            self.view_balance_withdrawGUI()
        



            self.withdraw_window.protocol("WM_DELETE_WINDOW",self.on_withdraw_close)

        except Exception as e :
            messagebox.showerror("Error", f"Failed to Withdraw: {str(e)}",parent=self.withdraw_window)
            


    def withdraw_function(self):
            try: 
                amount= int(self.withdraw_amount_entry.get())
                if amount is None or amount <= 0:
                    messagebox.showerror("Error", "Invalid amount.",parent=self.withdraw_canvas)
                    return

                if isinstance(amount,float):
                    messagebox.showerror("Error!","You cannot Withdraw cents!")
                    return
                
                if isinstance(amount,int) and not amount %10 == 0:
                    messagebox.showerror("Error!","Please enter a valid amount.\n(Only enter Note values , No coin values.)" )
                    return
                current_balance = int(self.get_balance_from_csv(self.account_no))
                if current_balance is None:
                    return  
                
                if amount > current_balance:
                    messagebox.showerror("Error", "Insufficient funds.",parent=self.LoginMenu_canvas)
                    return

                confirmation=messagebox.askyesno("Confirm Withdrawal",f"Are you sure you would like to withdraw R{amount}")
                if confirmation:
                    self.update_balance(-amount,self.account_no)
                    self.write_transaction("Withdraw", amount)

                    self.event_label=tk.Label(self.withdraw_canvas, text=f"Successfully withdrew\nR{amount:.2f} ", font=("Arial", 17) , fg="#aee6e6" , bg="#142133")
                    self.event_label.place(relx=0.5, rely=0.25,anchor="center")
                    self.withdraw_window.after(10000, self.event_label.destroy)
                
                self.withdraw_amount_entry.delete(0,tk.END)
                self.view_balance_withdrawGUI()

            except ValueError:
                messagebox.showerror("Error", "Invalid amount.")
                

    def on_withdraw_close(self):
        self.withdraw_window.destroy()
        self.LoginMenu.deiconify()
        self.LoginMenu.create_widgets()

    def transfer_GUI(self):
        try:
            self.LoginMenu.iconify()
            account_no =self.account_no
            self.transfer_window = tk.Toplevel()
            self.transfer_window.title("Transfer")
            self.transfer_window.resizable(False, False)
            window_width = 500
            window_height = 600

            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            center_x = int(screen_width / 2 - window_width / 2)
            center_y = int(screen_height / 2 - window_height / 2)

            self.transfer_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

            self.transfer_canvas = tk.Canvas(self.transfer_window, width=800, height=600)
            self.transfer_canvas.pack(fill="both", expand=True)
            
            self.transfer_background_image = Image.open("background.png")
            self.transfer_logo_image = Image.open("logo_transparent.png")
           
    
            self.transfer_background_photo = ImageTk.PhotoImage(self.transfer_background_image.resize((2000, 2000)))
            self.transfer_logo_photo = ImageTk.PhotoImage(self.transfer_logo_image.resize((100,100)))

            self.transfer_back_button = tk.Button(self.transfer_canvas, text="Back", command = self.on_transfer_close ,font =("Times New Roman", 17,"bold"),bg="#230e11", fg="#FFFFFF")
            self.transfer_back_button.place(relx=0.5, rely=0.9, anchor="center", width=80 , height=50)

            self.transfer_confirm_button = tk.Button(self.transfer_canvas, text="Transfer", command = self.transfer_function ,font =("Times New Roman", 15,"bold"),bg="#8a9099", fg="#FFFFFF")
            self.transfer_confirm_button.place(relx=0.5, rely=0.8, anchor="center", width=100 , height=50)

            
            
            self.transfer_name_background= tk.Button(self.transfer_canvas, state="disabled",font=("Times New Roman", 25,"bold"),bg="#090f16", fg="#FFFFFF")
            self.transfer_name_background.place(relx=0.5, rely=0.1, anchor="center", width=200 , height=50)

            self.transfer_name_label = tk.Label(self.transfer_canvas, text="Recipient's Name:", font=("Times New Roman", 18) , fg="#789aa2" , bg="#090f16")
            self.transfer_name_label.place(relx=0.5, rely=0.1,anchor="center")
            self.transfer_name_entry = tk.Entry(self.transfer_canvas,font=("Times New Roman", 20))
            self.transfer_name_entry.configure(bg="#2c3747",fg="#FFFFFF", justify="center")
            self.transfer_name_entry.place(relx=0.5, rely=0.2 , anchor="center" , width=200 , height=30)

            self.transfer_acc_background= tk.Button(self.transfer_canvas, state="disabled",font=("Times New Roman", 25,"bold"),bg="#090f16", fg="#FFFFFF")
            self.transfer_acc_background.place(relx=0.5, rely=0.3, anchor="center", width=350 , height=50)

            self.transfer_acc_label = tk.Label(self.transfer_canvas, text="Recipient's Account Number:", font=("Times New Roman", 18) , fg="#789aa2" , bg="#090f16")
            self.transfer_acc_label.place(relx=0.5, rely=0.3,anchor="center")
            self.transfer_acc_entry = tk.Entry(self.transfer_canvas,font=("Times New Roman", 20))
            self.transfer_acc_entry.configure(bg="#2c3747",fg="#FFFFFF", justify="center")
            self.transfer_acc_entry.place(relx=0.5, rely=0.4 , anchor="center" , width=200 , height=30)

            self.transfer_amount_background= tk.Button(self.transfer_canvas, state="disabled",font=("Times New Roman", 25,"bold"),bg="#090f16", fg="#FFFFFF")
            self.transfer_amount_background.place(relx=0.5, rely=0.58, anchor="center", width=200 , height=50)

            self.transfer_amount_label = tk.Label(self.transfer_canvas, text="Transfer Amount:", font=("Times New Roman", 18) , fg="#789aa2" , bg="#090f16")
            self.transfer_amount_label.place(relx=0.5, rely=0.58,anchor="center")
            self.transfer_amount_entry = tk.Entry(self.transfer_canvas,font=("Times New Roman", 30))
            self.transfer_amount_entry.configure(bg="#2c3747",fg="#FFFFFF", justify="center")
            self.transfer_amount_entry.place(relx=0.5, rely=0.68 , anchor="center" , width=200 , height=50)


            self.transfer_canvas.create_image(0, 0, image=self.transfer_background_photo, anchor=tk.NW)
            self.transfer_canvas.create_image(470,570, image=self.transfer_logo_photo, anchor=tk.SE)
        except:
            print()

    def transfer_function(self):
        try:
            transfer_recipient_user = self.transfer_name_entry.get().strip().lower()
            recipient_account_no = self.transfer_acc_entry.get().strip().lower()
            amount = int(self.transfer_amount_entry.get().strip().lower())
            valid_account=False
            if not transfer_recipient_user or not recipient_account_no or not amount or amount <= 0:
                messagebox.showerror("Error", "Invalid input.",parent=self.LoginMenu_canvas)
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
                    messagebox.showerror("Error", "Insufficient funds.",parent=self.LoginMenu_canvas)
                    return 
                
                if self.update_balance(-amount,self.account_no):
                    self.write_transaction("Transfer", amount , transfer_recipient_user.lower(), recipient_account_no)
                    self.update_balance(amount,recipient_account_no)
                    messagebox.showinfo("Transfer", f"R{amount:.2f} successfully transferred to {transfer_recipient_user}.", parent=self.LoginMenu_canvas)
                    extra_transfer=messagebox.askyesno("Perfrom Another Transfer?","Would you like to perform another transfer?",parent=self.transfer_window)
                    if extra_transfer:
                        self.transfer_name_entry.delete(0, tk.END)
                        self.transfer_acc_entry.delete(0, tk.END)
                        self.transfer_amount_entry.delete(0, tk.END)
                    else:
                        self.transfer_window.destroy()
                        self.LoginMenu.deiconify()
                        return
            else:
                messagebox.showerror("Error","The account number provided does not match any account in our database!\nPlease try again.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.",parent=self.LoginMenu_canvas)

    def on_transfer_close(self):
        self.transfer_window.destroy()
        self.LoginMenu.deiconify()
        self.LoginMenu.create_widgets()

    def view_transactions(self):
        try:
            self.LoginMenu.iconify()
            account_no =self.account_no
            self.transactions_window = tk.Toplevel()
            self.transactions_window.title("Transaction History")
            self.transactions_window.resizable(False, False)
            window_width = 900
            window_height = 700

            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()

            center_x = int(screen_width / 2 - window_width / 2)
            center_y = int(screen_height / 2 - window_height / 2)

            self.transactions_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

            self.transaction_canvas = tk.Canvas(self.transactions_window, width=800, height=600)
            self.transaction_canvas.pack(fill="both", expand=True)
            
            self.transaction_background_image = Image.open("background.png")
            self.transaction_logo_image = Image.open("logo_transparent.png")
           
            
            self.transaction_background_photo = ImageTk.PhotoImage(self.transaction_background_image.resize((2000, 2000)))
            self.transaction_logo_photo = ImageTk.PhotoImage(self.transaction_logo_image.resize((100,100)))

            self.transcation_back_button = tk.Button(self.transaction_canvas, text="Back", command = self.on_transaction_close ,font =("Times New Roman", 17,"bold"),bg="#230e11", fg="#FFFFFF")
            self.transcation_back_button.place(relx=0.5, rely=0.8, anchor="center", width=80 , height=50)

            self.transaction_canvas.create_image(0, 0, image=self.transaction_background_photo, anchor=tk.NW)
            self.transaction_canvas.create_image(850,650, image=self.transaction_logo_photo, anchor=tk.SE)

            transactions_text = scrolledtext.ScrolledText(self.transaction_canvas, width=100, height=30, wrap = tk.WORD)
            transactions_text.configure(fg="#FFFFFF", bg="#142133")
            transactions_text.pack(padx=20, pady=20)
            self.transactions_window.protocol("WM_DELETE_WINDOW",self.on_transaction_close)

            

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
            
            transactions_text.configure(state="disabled") 

            
            

        except FileNotFoundError:
            messagebox.showerror("Error", "Transaction log file not found.",parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view transactions: {str(e)}",parent=self.transaction_canvas)

        


    def on_transaction_close(self):
        self.transactions_window.destroy()
        self.LoginMenu.deiconify()
        self.LoginMenu.create_widgets()
        
    def write_transaction(self, transaction_type, amount, to_account=None, to_account_no=None):
        try:
            transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            from_account_name = str(self.current_user.capitalize())
            from_account_no = self.account_no

            if transaction_type == "Transfer" and to_account and to_account_no:
                transaction_details = f" {transaction_time} | {transaction_type}: R{amount:.2f} | From: {from_account_name} [{from_account_no}] to {to_account.capitalize()} [{to_account_no}]\n"
            else:
                transaction_details = f" {transaction_time} | {transaction_type}: R{amount:.2f} | From: {from_account_name} [{from_account_no}]\n"

            with open(self.transactions_log, "a") as file:
                file.write(transaction_details)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to write transaction: {str(e)}",parent=self.LoginMenu)

    def update_balance(self, amount,acc_no):
        try:
            account_no= int(acc_no)
           
            df = pd.read_csv(self.accounts_file, dtype={'id_number': str})
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
 