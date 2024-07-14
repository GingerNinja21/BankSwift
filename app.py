import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import file
import csv
from PIL import Image, ImageTk
from file import LoginValidation
from bankswift import BankingApplicationGUI



class AnimatedGIF(tk.Label):
    def __init__(self, master, gif_path, static_image_path, width, height, delay=100):
        super().__init__(master)
        self.master = master
        self.delay = delay
        self.gif_path = gif_path
        self.static_image_path = static_image_path
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
            frame_image = ImageTk.PhotoImage(image.copy().resize((self.width, self.height), Image.LANCZOS))
            self.frames.append(frame_image)

    def load_static_image(self):
        image = Image.open(self.static_image_path)
        image = image.resize((self.width, self.height), Image.LANCZOS)
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


class WelcomeWindow:     
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BankSwift")
        self.root.configure(bg="#052944")
        self.logo_gif="BANKSWIFT.gif"
        self.logo_static = "logo.png"
       
        window_width = 300
        window_height = 400

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.create_widgets()
        self.root.mainloop()
        

    def initialize_logo(self):
        self.animated_gif = AnimatedGIF(self.root, self.logo_gif, self.logo_static, 200, 200, 100)
        self.animated_gif.place(relx=0.5, rely=0.3 , anchor="center")
    
    def create_widgets(self):

        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        try:
            self.initialize_logo()
        except Exception as e:
            print()

        
       
        message_label = tk.Label(self.root, text="Dont have an Account?", fg="#37B7C3" , bg="#052944")
        message_label.place(relx=0.5 , rely=0.8 , anchor="center")
        

        register_link = tk.Label(self.root, text="Register here.", fg="white", bg = "#052944" ,cursor="hand2")
        register_link.place(relx=0.5, rely=0.9,anchor="center")
        register_link.bind("<Button-1>", lambda event: self.open_create_account())


        login_btn = tk.Button(self.root, text="Login", command=self.open_login, bg="#2196F3", fg="white", padx=20, pady=10)
        login_btn.place(relx=0.5, rely=0.65, anchor="center")
    
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
        self.root.destroy()
 
    def open_create_account(self):
        self.root.lower()
        CreateAccountWindow()
 
    def open_login(self):
        self.root.lower()
        LoginWindow()
 
class CreateAccountWindow:
    def __init__(self, ):
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
        
        self.background_image = Image.open("background.png")
        self.logo_image = Image.open("logo_transparent.png")
        self.banner_image = Image.open("Create_Account_Banner.png")
        
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((2000, 2000)))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image.resize((100,100)))
        self.banner_photo = ImageTk.PhotoImage(self.banner_image.resize((600, 100)))
        
        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)
        self.canvas.create_image(750, 550, image=self.logo_photo, anchor=tk.SE)

        self.create_widgets()
        # self.create_account.mainloop()

    def create_account_function(self):
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        id_no = self.id_entry.get().strip()
        phone_number = self.phone_entry.get().strip()
        email = self.email_entry.get().strip().lower()
        password = self.password_entry.get()
        pin = self.pin_entry.get().strip()
        balance = self.balance_entry.get().strip()
        account_type= self.account_type.get().strip().lower()
        validator = file.DataValidation(name, surname, id_no, email,phone_number,pin,balance,account_type)
        

        if not name or not surname or not id_no or not email :
            messagebox.showerror("Validation Error", "All fields are required!")
            return
        
        validator.account_existence()

        if validator.error_message :
            messagebox.showerror("Validation Error", validator.error_message)
            return
        
        if validator.invalid_username_id_pair:
            messagebox.showerror("Validation Error", validator.invalid_username_id_pair)
            return

        if validator.existing_user_id_acc_creation_message:
                response = messagebox.askyesno("ID number already exists in database", validator.existing_user_id_acc_creation_message) 
                if response:
                    file_writer = file.account_creation(name,surname,id_no,pin,phone_number,password,email,balance,account_type)
                    file_writer.store_account()
                    
                    login_question = messagebox.askyesno("Log in?", "Would you like to log in?")
                    if login_question:
                        self.create_account.destroy()
                        LoginWindow()
                        return
                    else:
                        self.go_back()
                        return
                else:
                    login_question = messagebox.askyesno("Log in?", "Would you like to log in instead?")
                    if login_question:
                        self.create_account.destroy()
                        LoginWindow(self)
                        return
                    
                    else:  
                        messagebox.showerror("Validation Error", "Account Already Exists!")
                        return      
        else:

            file_writer = file.account_creation(name,surname,id_no,pin,phone_number,password,email,balance,str(account_type))
            file_writer.store_account()
            file_writer.store_passwords()
            messagebox.showinfo("Success", "Account created successfully.")
            response = messagebox.askyesno("Login", "Would you like to log in?") 
            if response:
                self.create_account.destroy()
                LoginWindow(self)
            
            else:
                self.go_back()
            

    def create_widgets(self):
        
        banner_label=tk.Label(self.create_account, text="CREATE ACCOUNT:",font=("Times New Roman", 30) ,fg="#37B7C3" , bg="#142133")
        banner_label.place(relx=0.5, rely=0.1 ,anchor="center")

        name_label = tk.Label(self.create_account, text="Name:",font=("Trebuchet MS", 16) ,fg="#FFFFFF" , bg="#142133")
        name_label.place(relx=0.3, rely=0.2, anchor="center")
        self.name_entry = tk.Entry(self.create_account)
        self.name_entry.configure(bg="#2c3747")
        self.name_entry.configure(fg="#FFFFFF")
        self.name_entry.place(relx=0.6, rely=0.2,anchor="center")
 
        surname_label = tk.Label(self.create_account,text="Surname:", fg="#FFFFFF",font=("Trebuchet MS", 16)  , bg="#142133")
        surname_label.place(relx=0.3, rely=0.25,anchor="center")
        self.surname_entry = tk.Entry(self.create_account)
        self.surname_entry.configure(bg="#2c3747")
        self.surname_entry.configure(fg="#FFFFFF")
        self.surname_entry.place(relx=0.6, rely=0.25,anchor="center")
 
        id_label = tk.Label(self.create_account, text="ID No.:", fg="#FFFFFF",font=("Trebuchet MS", 16)  , bg="#142133")
        id_label.place(relx=0.3, rely=0.3,anchor="center")
        self.id_entry = tk.Entry(self.create_account)
        self.id_entry.configure(bg="#2c3747")
        self.id_entry.configure(fg="#FFFFFF")
        self.id_entry.place(relx=0.6, rely=0.3,anchor="center")
 
        phone_label = tk.Label(self.create_account, text="Phone:", fg="#FFFFFF" ,font=("Trebuchet MS", 16) , bg="#142133")
        phone_label.place(relx=0.3, rely=0.35,anchor="center")
        self.phone_entry = tk.Entry(self.create_account)
        self.phone_entry.configure(bg="#2c3747")
        self.phone_entry.configure(fg="#FFFFFF")
        self.phone_entry.place(relx=0.6, rely=0.35,anchor="center")
 
        email_label = tk.Label(self.create_account, text="Email:",font=("Trebuchet MS", 16) , fg="#FFFFFF" , bg="#142133")
        email_label.place(relx=0.3, rely=0.4,anchor="center")
        self.email_entry = tk.Entry(self.create_account)
        self.email_entry.configure(bg="#2c3747")
        self.email_entry.configure(fg="#FFFFFF")
        self.email_entry.place(relx=0.6, rely=0.4,anchor="center")
        

        account_type_label = tk.Label(self.create_account, text="Account Type:",font=("Trebuchet MS", 16)  , fg="#FFFFFF" , bg="#142133")
        account_type_label.place(relx=0.3, rely=0.45,anchor="center")
        self.account_type = tk.StringVar(value="Cheque")
        cheque_radio = tk.Radiobutton(self.create_account, text="Cheque",font=("Times New Roman", 14 ,"bold"), variable=self.account_type, value="cheque",fg ="#727a85" , bg="#142133")
        cheque_radio.place(relx=0.5, rely=0.45,anchor="center")
        savings_radio = tk.Radiobutton(self.create_account, text="Savings",font=("Times New Roman", 14 ,"bold"),variable=self.account_type, value="savings", fg = "#727a85" , bg="#142133")
        savings_radio.place(relx=0.7, rely=0.45,anchor="center")


        balance_label = tk.Label(self.create_account, text="Opening Balance:",font=("Trebuchet MS", 16) , fg="#FFFFFF" , bg="#142133")
        balance_label.place(relx=0.3, rely=0.5,anchor="center")
        self.balance_entry = tk.Entry(self.create_account)
        self.balance_entry.configure(bg="#2c3747")
        self.balance_entry.configure(fg="#FFFFFF")
        self.balance_entry.place(relx=0.6, rely=0.5,anchor="center")
 
        pin_label = tk.Label(self.create_account, text="Pin Number:",font=("Trebuchet MS", 16) , fg="#FFFFFF" , bg="#142133")
        pin_label.place(relx=0.3, rely=0.55,anchor="center")
        self.pin_entry = tk.Entry(self.create_account, show="*")
        self.pin_entry.configure(bg="#2c3747")
        self.pin_entry.configure(fg="#FFFFFF")
        self.pin_entry.place(relx=0.6, rely=0.55,anchor="center")
 
        password_label = tk.Label(self.create_account, text="Password:",font=("Trebuchet MS", 16) , fg="#FFFFFF" , bg="#142133")

        password_label.place(relx=0.3, rely=0.6,anchor="center")
        self.password_entry = tk.Entry(self.create_account,bg="#2c3747",fg="#FFFFFF")
        self.password_entry.place(relx=0.6, rely=0.6,anchor="center")
        
       
        generate_btn = tk.Button(self.create_account, text="Generate" , command=self.generate_password, bg="#37B7C3", fg="white", padx=1, pady=1)
        generate_btn.place(relx=0.8, rely=0.6,anchor="center")
 
        self.strength_label = tk.Label(self.create_account, text="Password Strength:",font=("Trebuchet MS", 16) ,fg="#FFFFFF" , bg="#142133")
        self.strength_label.place(relx=0.3, rely=0.65,anchor="center")
        self.strength_bar = ttk.Progressbar(self.create_account, mode="determinate", length=200)
        self.strength_bar.place(relx=0.6, rely=0.65,anchor="center")
 

 
        create_btn = tk.Button(self.create_account, text="Create Account",font=("Trebuchet MS", 16 , "bold") , command=self.create_account_function, bg="#8a9099", fg="#142133", padx=20, pady=10)
        create_btn.place(relx=0.5, rely=0.8, anchor="center")
 
        back_btn = tk.Button(self.create_account, text="Back", command=self.go_back, bg="#FF5722", fg="white", padx=20, pady=10)
        back_btn.place(relx=0.5, rely=0.9, anchor="center")
 
        self.create_account.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_account.mainloop()
 
    def on_close(self):
        self.create_account.destroy()
         

    def go_back(self):
        self.create_account.destroy()
 
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
 

class LoginWindow:
    def __init__(self):
        global recipient_name
        global accounts_file
        global banks_file
        global transaction_log

        
        
        accounts_file= "accounts.csv"
        banks_file= "banks.csv"
        transaction_log = "transactionslog.txt"
    
        self.login = tk.Toplevel()
        self.login.title("Login")
        self.login.configure(bg="#071952")

        window_width = 800
        window_height = 600

        screen_width = self.login.winfo_screenwidth()
        screen_height = self.login.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.login.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.create_widgets()

    def create_widgets(self):
        name_label = tk.Label(self.login, text="Name:", fg="#37B7C3", bg="#071952")
        name_label.place(relx=0.1, rely=0.2)
        self.name_entry = tk.Entry(self.login)
        self.name_entry.place(relx=0.3, rely=0.2)

        email_label = tk.Label(self.login, text="Email:", fg="#37B7C3", bg="#071952")
        email_label.place(relx=0.1, rely=0.3)
        self.email_entry = tk.Entry(self.login, width=30)
        self.email_entry.place(relx=0.3, rely=0.3)

        pin_label = tk.Label(self.login, text="Pin:", fg="#37B7C3", bg="#071952")
        pin_label.place(relx=0.1, rely=0.4)
        self.pin_entry = tk.Entry(self.login, show="*")
        self.pin_entry.place(relx=0.3, rely=0.4)

        id_label = tk.Label(self.login, text="ID Number:", fg="#37B7C3", bg="#071952")
        id_label.place(relx=0.1, rely=0.5)
        self.id_entry = tk.Entry(self.login)
        self.id_entry.place(relx=0.3, rely=0.5)

        login_btn = tk.Button(self.login, text="Login", command=self.login_function, bg="#4CAF50", fg="white",
                              padx=20, pady=10)
        login_btn.place(relx=0.5, rely=0.7, anchor="center")

        forgot_pin_link = tk.Label(self.login, text="Forgot Pin?", fg="#EBF4F6", bg="#071952", cursor="hand2")
        forgot_pin_link.place(relx=0.6, rely=0.4)
        forgot_pin_link.bind("<Button-1>", lambda event: self.forgot_pin())

        back_btn = tk.Button(self.login, text="Back", command=self.go_back, bg="#FF5722", fg="white", padx=20, pady=10)
        back_btn.place(relx=0.3, rely=0.7, anchor="center")
        
        self.login.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.login.destroy()
        

    def go_back(self):
        self.login.destroy()

    def validate_entries(self):
        email = self.email_entry.get().strip().lower()
        pin = self.pin_entry.get().strip()
        id_no = self.id_entry.get().strip()

        if not email or not pin or not id_no:
            messagebox.showerror("Error", "Email, Pin, and ID Number are required")
            return False
        return True

    def forgot_pin(self):
        email = self.email_entry.get().strip().lower()
        id_no = self.id_entry.get().strip()

        if not email or not id_no:
            messagebox.showerror("Error", "Email and ID Number are required to recover pin.")
            return

        validator = LoginValidation(email, id_no, "")

        recovery_result = validator.password_recovery()
        messagebox.showinfo("Password Recovery", recovery_result)

    def login_function(self):
        email = self.email_entry.get().strip().lower()
        pin = self.pin_entry.get().strip()
        global name
        global id_no
        id_no = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        account_exists= False
        

        if self.validate_entries():
            try:
                with open('password_records.csv', mode='r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if (email == row['email'].strip().lower() and
                                name == row["name"].strip().lower() and
                                pin == row['pin'].strip() and
                                id_no == row['id'].strip()):
                            account_exists= True
                            messagebox.showinfo("Success", "Login successful.")
                            
                            if account_exists:
                                self.login.destroy()
                                DashboardWindow()
                                return 
                        
                    messagebox.showerror("Error", "Invalid credentials. Please try again.")
            except FileNotFoundError:
                messagebox.showerror("Error", "Password records file not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")


class DashboardWindow:
    
    def __init__(self):    
        global id_no
        global name
        
        accounts_file = "accounts.csv"
        banks_file = "banks.csv"
        transactions_log = "transactionslog.txt"
        
        BankingApplicationGUI(name, accounts_file, banks_file, transactions_log, id_no)

    def on_close(self):
        self.dashboard.destroy()   
 
if __name__ == "__main__":
    app= WelcomeWindow()
    app.root.mainloop()
 