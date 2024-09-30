import tkinter as tk
from tkinter import ttk , messagebox ,scrolledtext, messagebox, simpledialog
import random
import string
import file2_0
import pandas as pd
import csv
from PIL import Image, ImageTk
from file2_0 import LoginValidation,DataValidation, account_creation
from LoginGUI2_0 import BankingApplicationGUI
import subprocess
import sys
import os




logo_gif="images/BANKSWIFT.gif"
logo_static = "images/logo.png"



class app():
    # home screen
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BankSwift")
        self.root.configure(bg="#052944")
        self.logo_gif="images/BANKSWIFT.gif"
        self.logo_static = "images/logo.png"
       
        window_width = 800
        window_height = 600

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)

        self.create_widgets()

        self.root.grab_set()
        
    def initialize_logo(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        

        self.background_image = Image.open("images/background.png")   
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((2000, 2000)))
        background_photo = tk.Label(image=self.background_photo)
        

        self.animated_gif = AnimatedGIF(self.root, logo_gif, logo_static, 200, 200, 100)
        self.animated_gif.place(relx=0.5, rely=0.3 , anchor="center")
        background_photo.place(relx=0,rely=0,anchor="nw")

       
       
    def create_widgets(self):

        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        try:
            self.initialize_logo()
            

        except Exception as e:
            pass  

        

        home_banner_label1=tk.Label(self.root, fg="#37B7C3" , bg="#090f16")
        home_banner_label1.place(relx=0.5, rely=0.95 ,anchor="center" , width=799 , height=60)

        home_banner_label2=tk.Label(self.root,fg="#FFFFFF", bg="#0a1627")
        home_banner_label2.place(relx=0.5, rely=0.995 ,anchor="center", width=799, height=5)  

        home_banner_label3=tk.Label(self.root,fg="#FFFFFF", bg="#0a1627")
        home_banner_label3.place(relx=0.5, rely=0.90 ,anchor="center", width=799 , height=5)  

        slogan_label1= tk.Label(self.root, text="Bank Smart , Bank Efficient , ",font=("Lucida Sans Unicode", 12 ), fg="#2e6b7f" , bg="#090f16")  
        slogan_label1.place(relx=0.45 , rely=0.95 , anchor="center" , height=20) 
        
        slogan_label2= tk.Label(self.root, text="BankSwift.",font=("Times New Roman", 14,), fg="#0897f3" , bg="#090f16")  
        slogan_label2.place(relx=0.64 , rely=0.951 , anchor="center" ,width=85 , height=20) 
       
        message_label = tk.Label(self.root, text="Dont have an Account?",font=("Times New Roman", 15), fg="#37B7C3" , bg="#142133")
        message_label.place(relx=0.5 , rely=0.75 , anchor="center")    
            
        register_link = tk.Label(self.root, text="Register here.", font=("Times New Roman", 12),fg="white", bg = "#142133" ,cursor="hand2")
        register_link.place(relx=0.5, rely=0.8,anchor="center")
        register_link.bind("<Button-1>", lambda event: self.open_create_account())

        login_btn = tk.Button(self.root, text="Login", command=self.open_login,  font=("Times New Roman", 15,"bold"), bg="#8a9099", fg="#142133", padx=20, pady=10)
        login_btn.place(relx=0.5, rely=0.65, anchor="center")


        

    def on_close(self):
        self.root.destroy()
 
    def open_create_account(self):
        self.root.iconify()
        self.CreateAccountWindow()
 
    def open_login(self):
        self.root.iconify()
        self.LoginWindow()






    # create account window
    def CreateAccountWindow(self):
        self.create_account = tk.Toplevel()
        self.create_account.title("Create Account")
        self.create_account.geometry("600x600")
        self.create_account.configure(bg="#052944")
        window_width = 800
        window_height = 600

        screen_width = self.create_account.winfo_screenwidth()
        screen_height = self.create_account.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.create_account.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        self.create_account.resizable(False, False)
        self.create_account.grab_set()

        self.canvas = tk.Canvas(self.create_account, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        
        self.background_image = Image.open("images/background.png")
        self.logo_image = Image.open("images/logo_transparent.png")
        
        
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((2000, 2000)))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image.resize((100,100)))
     

        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)
        self.canvas.create_image(750, 550, image=self.logo_photo, anchor=tk.SE)

        self.create_account_widgets()
        self.create_account.protocol("WM_DELETE_WINDOW", self.on_create_account_close)

    def create_account_widgets(self):
        account_banner_label=tk.Label(self.create_account, text="CREATE ACCOUNT:",font=("Times New Roman", 30) ,fg="#37B7C3" , bg="#090f16")
        account_banner_label.place(relx=0.5, rely=0.1 ,anchor="center" , width=780)

        name_label = tk.Label(self.create_account, text="Name:",font=("Times New Roman", 16) ,fg="#FFFFFF" , bg="#142133")
        name_label.place(relx=0.3, rely=0.2, anchor="center")
        self.name_entry = tk.Entry(self.create_account,width=40)
        self.name_entry.configure(bg="#2c3747")
        self.name_entry.configure(fg="#FFFFFF")
        self.name_entry.place(relx=0.6, rely=0.2,anchor="center")
 
        surname_label = tk.Label(self.create_account,text="Surname:", fg="#FFFFFF",font=("Times New Roman", 16)  , bg="#142133")
        surname_label.place(relx=0.3, rely=0.25,anchor="center")
        self.surname_entry = tk.Entry(self.create_account,width=40)
        self.surname_entry.configure(bg="#2c3747")
        self.surname_entry.configure(fg="#FFFFFF")
        self.surname_entry.place(relx=0.6, rely=0.25,anchor="center")
 
        id_label = tk.Label(self.create_account, text="ID No.:", fg="#FFFFFF",font=("Times New Roman", 16)  , bg="#142133")
        id_label.place(relx=0.3, rely=0.3,anchor="center")
        self.id_entry = tk.Entry(self.create_account,width=40)
        self.id_entry.configure(bg="#2c3747")
        self.id_entry.configure(fg="#FFFFFF")
        self.id_entry.place(relx=0.6, rely=0.3,anchor="center")
 
        phone_label = tk.Label(self.create_account, text="Phone:", fg="#FFFFFF" ,font=("Times New Roman", 16) , bg="#142133")
        phone_label.place(relx=0.3, rely=0.35,anchor="center")
        self.phone_entry = tk.Entry(self.create_account,width=40)
        self.phone_entry.configure(bg="#2c3747")
        self.phone_entry.configure(fg="#FFFFFF")
        self.phone_entry.place(relx=0.6, rely=0.35,anchor="center")
 
        email_label = tk.Label(self.create_account, text="Email:",font=("Times New Roman", 16) , fg="#FFFFFF" , bg="#142133")
        email_label.place(relx=0.3, rely=0.4,anchor="center")
        self.email_entry = tk.Entry(self.create_account,width=40)
        self.email_entry.configure(bg="#2c3747")
        self.email_entry.configure(fg="#FFFFFF")
        self.email_entry.place(relx=0.6, rely=0.4,anchor="center")
        

        account_type_label = tk.Label(self.create_account, text="Account Type:",font=("Times New Roman", 16)  , fg="#FFFFFF" , bg="#142133")
        account_type_label.place(relx=0.3, rely=0.45,anchor="center")
        self.account_type = tk.StringVar(value="Cheque")
        cheque_radio = tk.Radiobutton(self.create_account, text="Cheque",font=("Times New Roman", 14 ,"bold"), variable=self.account_type, value="cheque",fg ="#727a85" , bg="#142133")
        cheque_radio.place(relx=0.5, rely=0.45,anchor="center")
        savings_radio = tk.Radiobutton(self.create_account, text="Savings",font=("Times New Roman", 14 ,"bold"),variable=self.account_type, value="savings", fg = "#727a85" , bg="#142133")
        savings_radio.place(relx=0.7, rely=0.45,anchor="center")


        balance_label = tk.Label(self.create_account, text="Opening Balance:",font=("Times New Roman", 16) , fg="#FFFFFF" , bg="#142133")
        balance_label.place(relx=0.3, rely=0.5,anchor="center")
        self.balance_entry = tk.Entry(self.create_account,width=40)
        self.balance_entry.configure(bg="#2c3747")
        self.balance_entry.configure(fg="#FFFFFF")
        self.balance_entry.place(relx=0.6, rely=0.5,anchor="center")
 
        pin_label = tk.Label(self.create_account, text="Pin Number:",font=("Times New Roman", 16) , fg="#FFFFFF" , bg="#142133")
        pin_label.place(relx=0.3, rely=0.55,anchor="center")
        self.pin_entry = tk.Entry(self.create_account, show="*",width=40)
        self.pin_entry.configure(bg="#2c3747")
        self.pin_entry.configure(fg="#FFFFFF")
        self.pin_entry.place(relx=0.6, rely=0.55,anchor="center")
 
        account_password_label = tk.Label(self.create_account, text="Password:",font=("Times New Roman" ,16) , fg="#FFFFFF" , bg="#142133")
        account_password_label.place(relx=0.3, rely=0.6,anchor="center")
        self.account_password_entry = tk.Entry(self.create_account,bg="#2c3747",fg="#FFFFFF",state="readonly",width=40)
        self.account_password_entry.place(relx=0.6, rely=0.6,anchor="center")
        
       
        generate_btn = tk.Button(self.create_account, text="Generate" , command=self.generate_password, bg="#37B7C3", fg="white", padx=1, pady=1)
        generate_btn.place(relx=0.8, rely=0.6,anchor="center")
 
        self.strength_label = tk.Label(self.create_account, text="Password Strength:",font=("Times New Roman", 16) ,fg="#FFFFFF" , bg="#142133")
        self.strength_label.place(relx=0.3, rely=0.65,anchor="center")
        self.strength_bar = ttk.Progressbar(self.create_account, mode="determinate", length=250)
        self.strength_bar.place(relx=0.6, rely=0.65,anchor="center")
 

 
        create_btn = tk.Button(self.create_account, text="Create Account",font=("Times New Roman", 16 , "bold") , command=self.create_account_function, bg="#8a9099", fg="#142133", padx=20, pady=10)
        create_btn.place(relx=0.5, rely=0.8, anchor="center")
 
        create_back_btn = tk.Button(self.create_account, text="Back", command=self.go_back_create_account,font=("Times New Roman", 13 , "bold") ,bg="#230e11", fg="white", padx=20, pady=10)
        create_back_btn.place(relx=0.5, rely=0.9, anchor="center")
 
        self.create_account.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_account_function(self):
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        id_no = str(self.id_entry.get().strip())
        phone_number = self.phone_entry.get().strip()
        email = self.email_entry.get().strip().lower()
        password = self.account_password_entry.get()
        pin = self.pin_entry.get().strip()
        balance = self.balance_entry.get().strip()
        account_type= self.account_type.get().strip().lower()
        validator = file2_0.DataValidation(name, surname, id_no, email,phone_number,pin,balance,account_type)
        validator.account_existence()

        if not name or not surname or not id_no or not email or not pin or not password or not account_type:
            messagebox.showerror("Validation Error", "All fields are required!",parent=self.create_account)
            return
        
        if validator.error_message :
            messagebox.showerror("Validation Error", validator.error_message, parent=self.create_account)
            return
        
        if validator.invalid_username_id_pair:
            messagebox.showerror("Validation Error", validator.invalid_username_id_pair,parent=self.create_account)
            return
        
        if validator.account_existence():
            if validator.account_existence() and validator.existing_user_id_acc_creation_message:
                response = messagebox.askyesno("ID number already exists in database", validator.existing_user_id_acc_creation_message,parent=self.create_account) 
                if response:
                    file_writer = file2_0.account_creation(name,surname,id_no,pin,phone_number,password,email,balance,account_type)
                    file_writer.store_account()
                    
                    login_question = messagebox.askyesno("Log in?", "Would you like to log in?",parent=self.create_account)
                    if login_question:
                        self.create_account.destroy()
                        self.LoginWindow()
                        return
                    else:
                        self.go_back_create_account()
                        return
                else:
                    login_question = messagebox.askyesno("Log in?", "Would you like to log in instead?",parent=self.create_account)
                    if login_question:
                        self.create_account.destroy()
                        self.LoginWindow()
                        return
                    
                    else:  
                        messagebox.showerror("Validation Error", "Account Already Exists!",parent=self.create_account)
                        return

    
        
            else:
                messagebox.showerror("Validation Error", "Account Already Exists!",parent=self.create_account)
                return
        
        else:

            file_writer = file2_0.account_creation(name,surname,id_no,pin,phone_number,password,email,balance,str(account_type))
            file_writer.store_account()
            file_writer.store_passwords()
            messagebox.showinfo("Success", "Account created successfully.",parent=self.create_account)
            response = messagebox.askyesno("Login", "Would you like to log in?",parent=self.create_account) 
            if response:
                self.create_account.destroy()
                self.LoginWindow()
            
            else:
                self.go_back_create_account()
   
    def on_create_account_close(self):
        self.create_account.destroy()
        self.root.deiconify()
        self.create_widgets()
        
    def generate_password(self):
        self.account_password_entry.config(state="normal")
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(12))
        self.account_password_entry.configure(background="#142133", foreground="#000000")
        self.account_password_entry.delete(0, tk.END)
        self.account_password_entry.insert(0, password)
        self.account_password_entry.config(state="readonly")
        
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
       
    def go_back_create_account(self):
        self.create_account.destroy()
        self.root.deiconify()
        self.create_widgets()
        




    # login window
    def LoginWindow(self):
        self.login = tk.Toplevel()
        self.login.title("Login")
        
        self.login.configure(bg="#052944")

        window_width = 800
        window_height = 600

        screen_width = self.login.winfo_screenwidth()
        screen_height = self.login.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.login.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.login.resizable(False, False)
        

        self.canvas = tk.Canvas(self.login, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        
        self.background_image = Image.open("images/background.png")
        self.logo_image = Image.open("images/logo_transparent.png")
        
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((2000, 2000)))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image.resize((100,100)))
        

        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)
        self.canvas.create_image(750, 550, image=self.logo_photo, anchor=tk.SE)

        self.Login_widgets()    
        self.login.grab_set()
        self.login.protocol("WM_DELETE_WINDOW", self.on_login_close)
 
    def Login_widgets(self):


        log_banner_label=tk.Label(self.login, text="LOG IN",font=("Times New Roman", 30 ) ,fg="#0897f3" , bg="#090f16")
        log_banner_label.place(relx=0.5, rely=0.095 ,anchor="center" , width=790)
        log_banner2_label=tk.Label(self.login, text=f"Enter Your Details Below:",font=("Times New Roman", 15) ,fg="#37B7C3" , bg="#0a1627")
        log_banner2_label.place(relx=0.5, rely=0.16 ,anchor="center", width=790)



        login_name_label = tk.Label(self.login, text="Name:",font=("Times New Roman", 16) , fg="#FFFFFF" , bg="#142133")
        login_name_label.place(relx=0.5, rely=0.23,anchor="center")
        self.login_name_entry = tk.Entry(self.login)
        self.login_name_entry.configure(bg="#2c3747",font=("Lucida Sans", 13),fg="#FFFFFF", justify="center")
        self.login_name_entry.place(relx=0.5, rely=0.27 , width=400, anchor="center")

        login_email_label = tk.Label(self.login, text="Email:",font=("Times New Roman", 16) , fg="#FFFFFF" , bg="#142133")
        login_email_label.place(relx=0.5, rely=0.33,anchor="center")
        self.login_email_entry = tk.Entry(self.login)
        self.login_email_entry.configure(bg="#2c3747",font=("Lucida Sans", 13),fg="#FFFFFF", justify="center")
        self.login_email_entry.place(relx=0.5, rely=0.38,anchor="center",width=400)

        id_label = tk.Label(self.login, text="ID Number:", font=("Times New Roman", 16) , fg="#FFFFFF" , bg="#142133")
        id_label.place(relx=0.5, rely=0.43,anchor="center")
        self.login_id_entry = tk.Entry(self.login)
        self.login_id_entry.configure(bg="#2c3747",font=("Lucida Sans", 13),fg="#FFFFFF", justify="center")
        self.login_id_entry.place(relx=0.5, rely=0.48,anchor="center",width=400)

        login_pin_label = tk.Label(self.login, text="Pin:", font=("Times New Roman", 16) , fg="#FFFFFF" , bg="#142133")
        login_pin_label.place(relx=0.5, rely=0.53,anchor="center")
        self.login_pin_entry = tk.Entry(self.login, show="*",font=("Times New Roman", 30))
        self.login_pin_entry.configure(bg="#2c3747",fg="#FFFFFF", justify="center")
        self.login_pin_entry.place(relx=0.5, rely=0.63 , anchor="center",width=150,height=50)

        

        login_btn = tk.Button(self.login, text="Login", command=self.login_function,font=("Times New Roman", 14 ,"bold") ,bg="#8a9099", fg="#142133",padx=25, pady=20)
        login_btn.place(relx=0.57, rely=0.88, anchor="center")

        login_back_btn = tk.Button(self.login, text="Back", command=self.go_back_login,font=("Times New Roman", 14,"bold"), bg="#230e11", fg="white", padx=25, pady=20)
        login_back_btn.place(relx=0.4, rely=0.88, anchor="center")

        self.login.protocol("WM_DELETE_WINDOW", self.on_login_close)

        
    def validate__entries(self):
        name=self.login_name_entry.get().strip().lower()
        email = self.login_email_entry.get().strip().lower()
        pin = self.login_pin_entry.get().strip()
        id_no = self.login_id_entry.get().strip()

        if not email or not pin or not id_no or not name:
            messagebox.showerror("Error", "Name,Email, Pin, and ID Number are required", parent=self.login)
            return False
        return True

    def login_function(self):
        email = self.login_email_entry.get().strip().lower()
        pin = self.login_pin_entry.get().strip()
        global login_name
        global login_id_no
        login_id_no = self.login_id_entry.get().strip()
        login_name = self.login_name_entry.get().strip().lower()
        account_exists= False
        
        try:    
                
                    
                if self.validate__entries():
                    with open("userdata/passwordrecords.csv", mode='r') as csvfile:

                        
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            if (email == row['email'].strip().lower() and
                                    login_name == row["name"].strip().lower() and
                                    pin == row['pin'].strip() and
                                    login_id_no == row['id'].strip()):
                                account_exists= True
                                
                        if account_exists:
                            if self.acc_selector():
                                self.login.destroy()
                                return
                            else:
                                messagebox.showinfo("Success", "Login successful.",parent=self.login)
                                self.del_login_details()
                                self.login.iconify()
                                self.DashboardWindow()
                                
                                return
                                         
                                        
                                    
                                
                        messagebox.showerror("Error", "Account not found . \nCheck your acredentials and try again.",parent=self.login)
                        return
                else:                                                       
                     return                  
        except FileNotFoundError:
                messagebox.showerror("Error", "why1.",parent=self.login)
        except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}",parent=self.login)

    def del_login_details(self):
        self.login_email_entry.delete(0, tk.END)
        self.login_id_entry.delete(0, tk.END)
        self.login_name_entry.delete(0, tk.END)
        self.login_pin_entry.delete(0, tk.END)
           
    def on_login_close(self):
        self.login.destroy()
        self.root.deiconify()
        self.create_widgets()
        
    def go_back_login(self):
        self.login.destroy()
        self.root.deiconify()
        self.create_widgets()   
        
        




    # account select window
    def acc_selector(self):
        try:
            self.account_no=""
            self.acc_type=""
            acc_sel_id_no = self.login_id_entry.get().strip()
            accounts=[]
            account_types=[]
            self.multiple_accounts = False
            
            with open("userdata/accounts.csv", "r") as file:
                    for line in file:
                        parts = line.strip().split(",")
                        if len(parts) > 6  and acc_sel_id_no == parts[6] :
                            accounts.append(parts[3])
                            account_types.append(parts[5])
                            self.account_no = parts[3]
                            self.acc_type = parts[5]

                            if len(accounts)>1:
                                self.multiple_accounts= True


            if self.multiple_accounts:
                            self.login.destroy()
                            self.acc_sel_window = tk.Toplevel()
                            self.acc_sel_window.title("Account Selector")
                            self.acc_sel_window.resizable(False, False)
                            window_width = 500
                            window_height = 600

                            screen_width = self.root.winfo_screenwidth()
                            screen_height = self.root.winfo_screenheight()

                            center_x = int(screen_width / 2 - window_width / 2)
                            center_y = int(screen_height / 2 - window_height / 2)

                            self.acc_sel_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

                            self.acc_sel_canvas = tk.Canvas(self.acc_sel_window, width=800, height=600)
                            self.acc_sel_canvas.pack(fill="both", expand=True)
                            
                            self.acc_sel_background_image = Image.open("images/background.png")
                            self.acc_sel_logo_image = Image.open("images/logo_transparent.png")
                        
                    
                            self.acc_sel_background_photo = ImageTk.PhotoImage(self.acc_sel_background_image.resize((2000, 2000)))
                            self.acc_sel_logo_photo = ImageTk.PhotoImage(self.acc_sel_logo_image.resize((100,100)))

                            self.acc_sel_banner_label1=tk.Label(self.acc_sel_window, text="Accounts",font=("Times New Roman", 30) ,fg="#37B7C3" , bg="#090f16")
                            self.acc_sel_banner_label1.place(relx=0.5, rely=0.1 ,anchor="center" , width=495)

                            self.acc_sel_banner_label2=tk.Label(self.acc_sel_window , text="Select An Account:",font=("Times New Roman", 15) ,fg="#FFFFFF", bg="#0a1627")
                            self.acc_sel_banner_label2.place(relx=0.5, rely=0.16 ,anchor="center", width=495)



                           
                            self.acc_sel_canvas.create_image(0, 0, image=self.acc_sel_background_photo, anchor=tk.NW)
                            self.acc_sel_canvas.create_image(750, 550, image=self.acc_sel_logo_photo, anchor=tk.SE)
                            
                           

                            offset_y = 0.25  
                            
                            savings_row = 1
                            cheque_row = 1
                            num_buttons_savings = 0
                            num_buttons_cheque = 0
                            self.button_frame_savings = tk.Frame(self.acc_sel_canvas, bg="#0a1627")
                            self.scrollbar_savings = tk.Scrollbar(self.button_frame_savings, orient="vertical", command=self.acc_sel_canvas.yview)

                            self.button_frame_cheque = tk.Frame(self.acc_sel_canvas, bg="#0a1627")
                            self.acc_sel_canvas.create_window(50, offset_y * 600, anchor=tk.NW, window=self.button_frame_savings)
                            self.acc_sel_canvas.create_window(300, offset_y * 600, anchor=tk.NW, window=self.button_frame_cheque)

                            self.savings_label= tk.Label(self.button_frame_savings ,text="Savings" ,font=("Times New Roman" , 15 ,"bold"))
                            self.savings_label.grid(row=0 ,sticky="nsew")
                            self.cheque_label= tk.Label(self.button_frame_cheque ,text="Cheque" ,font=("Times New Roman" , 15 ,"bold"))
                            self.cheque_label.grid(row=0 ,sticky="nsew")

                            self.no_savings_accounts=0
                            self.no_cheque_accounts=0

                            savings_expand= False
                            for acc_ty in account_types:
                                if acc_ty == "savings":
                                    self.no_savings_accounts += 1
                                elif acc_ty =="cheque":
                                    self.no_cheque_accounts +=1
                                

                            for index, (account, acc_type) in enumerate(zip(accounts, account_types)):
    
                                if self.no_savings_accounts>3:
                                    savings_text=f"Account:\n{account}"
                                    savings_expand= True
                                
                                else:
                                    savings_text=f"Account:\n{account}"
                                    savings_expand=False
                                    

                                if acc_type == "savings":
                                        button_savings = tk.Button(self.button_frame_savings, text=savings_text)

                                        if savings_expand:
                                            button_savings.configure(font=("Times New Roman", 12,"bold"), bg="#090f16", fg="#FFFFFF", pady=5)
                                            button_savings.config(command=lambda acc=account, ac_ty=acc_type: self.set_account_number(acc, ac_ty))
                                            button_savings.grid(row=savings_row, column=0, padx=20, pady=10, sticky="nsew")
                                            savings_row += 1
                                        
                                        else:
                                            button_savings.configure(font=("Times New Roman", 12,"bold"), bg="#090f16", fg="#FFFFFF", pady=5)
                                            button_savings.config(command=lambda acc=account, ac_ty=acc_type: self.set_account_number(acc, ac_ty))
                                            button_savings.grid(row=savings_row, column=0, padx=20, pady=10, sticky="nsew")
                                            savings_row += 1

                                        
                                else:   
                                        button_cheque = tk.Button(self.button_frame_cheque, text=f"{account}\n{acc_type.capitalize()}")
                                        button_cheque.configure(font=("Times New Roman", 12, "bold"), bg="#090f16", fg="#FFFFFF", pady=5)
                                        button_cheque.config(command=lambda acc=account, ac_ty=acc_type: self.set_account_number(acc, ac_ty))
                                        button_cheque.grid(row=cheque_row, column=0, padx=20, pady=10, sticky="nsew")
                                        cheque_row += 1
                                    
                            
                            self.acc_sel_back_button = tk.Button(self.acc_sel_canvas, text="Log Out" ,font =("Times New Roman", 17,"bold"),bg="#230e11", fg="#FFFFFF" , command=self.on_acc_sel_close)
                            self.acc_sel_back_button.place(relx=0.5, rely=0.9, anchor="center", width=100 , height=50)

                            
                            self.acc_sel_window.grab_set()

                            self.acc_sel_window.protocol("WM_DELETE_WINDOW" , self.on_acc_sel_close )
                           
                            return True
        
                           
            return False
                            
            
        except Exception as e:
            print(f"smth when wrong : {str(e)}")
    
    def set_account_number(self,account,acc_type):
        self.account_no = account 
        self.acc_type = acc_type
        self.acc_sel_window.iconify()
        self.DashboardWindow()
   
    def on_acc_sel_close(self):
        if messagebox.askyesno("LOG OUT?", "Are you sure you want to log out?"):
            self.acc_sel_window.destroy()
            self.LoginWindow()
        else:
            return

    





    # dashboard
    def DashboardWindow(self):
        global login_id_no
        global login_name
            
        accounts_file = "userdata/accounts.csv"
        banks_file = "banks.csv"
        transactions_log = "transactionslog.txt"

        if self.multiple_accounts:
            BankingApplicationGUI(self.acc_sel_window,login_name, login_id_no,banks_file, transactions_log ,self.account_no,self.multiple_accounts)

            
        else:
            BankingApplicationGUI(self.login,login_name, login_id_no,banks_file, transactions_log ,self.account_no)
      




    # home screeen GIF
class AnimatedGIF(tk.Label):
    def __init__(self, master, gif_path, static_image_path, width, height, delay=100):
        super().__init__(master,borderwidth=0,highlightbackground="#212b52",highlightthickness=3 )
        self.master = master
        self.delay = delay
        self.gif_path = gif_path
        self.gif_path = gif_path
        self.static_image_path = static_image_path
        self.static_image_path=static_image_path
        self.width = width
        self.height = height
        self.frames = []
        self.load_frames()
        self.static_image = self.load_static_image()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.config(image=self.image)
        self.animate()
        

    def load_frames(self):
        image = Image.open(self.gif_path)
        for frame in range(0, image.n_frames):
            image.seek(frame)
            frame_image = ImageTk.PhotoImage(image.copy().resize((self.width, self.height), Image.Resampling.LANCZOS))
            self.frames.append(frame_image)

    def load_static_image(self):
        image = Image.open(self.static_image_path)
        image = image.resize((self.width, self.height), Image.Resampling.LANCZOS )
        return ImageTk.PhotoImage(image)

    def animate(self):

        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 2  
            if self.current_frame >= len(self.frames):
                self.current_frame = len(self.frames) - 1 
            self.config(image=self.frames[self.current_frame])
            self.after(self.delay, self.animate)
        else:
            self.config(image=self.static_image)


 
 
if __name__ == "__main__":
    x= app()
    # x.LoginWindow
    x.root.mainloop()
 