import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import file
import csv
from PIL import Image, ImageTk
from file import LoginValidation
import bankswift

recipient_name=""
accounts_file=""
accounts_file=""
banks_file=""
transaction_log=""
class AnimatedGIF(tk.Label):
    def __init__(self, master, gif_path, static_image_path, width, height, delay=100):
        super().__init__(master)
        self.master = master
        self.delay = delay
        self.gif_path = gif_path
        self.gif_path = "BANKSWIFT.gif"
        self.static_image_path = static_image_path
        self.static_image_path="logo.png"
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
        image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def animate(self):

        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 2  # Increase by 2 frames to speed up the animation
            if self.current_frame >= len(self.frames):
                self.current_frame = len(self.frames) - 1  # Ensure it doesn't go out of bounds
            self.config(image=self.frames[self.current_frame])
            self.after(self.delay, self.animate)
        else:
            self.config(image=self.static_image)


class WelcomeWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BankSwift")
        self.root.configure(bg="#071952")
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
        self.animated_gif.grid(row=5 , column=2)
        self.animated_gif.pack()
    
    def create_widgets(self):
        # if all fails
        # image = Image.open("logo.png")  # Replace with your image file path
        # resized_image=image.resize((200, 200),)
        # photo = ImageTk.PhotoImage(resized_image)
        # self_logo = tk.Label(self.root,image=photo)
        # self_logo.grid(row=5 ,column=2)
        # self_logo.pack()
        self.initialize_logo()
        Register = tk.Label(self.root, text="Dont have an Account?", fg="#37B7C3" , bg="#071952")
        Register.place(relx=0.1 , rely=0.8)

        register_link = tk.Label(self.root, text="Register here.", fg="white", bg = "#01204E" ,cursor="hand2")
        register_link.place(relx=0.6, rely=0.8)
        register_link.bind("<Button-1>", lambda event: self.open_create_account())

        # create_account_btn = tk.Button(self.root, text="Create Account", command=self.open_create_account, bg="#4CAF50", fg="white", padx=20, pady=10)
        # create_account_btn.place(relx=0.5, rely=0.6, anchor="center")
 
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
        self.root.withdraw()
 
    def open_create_account(self):
        self.root.withdraw()
        CreateAccountWindow(self)
 
    def open_login(self):
        self.root.withdraw()
        LoginWindow(self)

    def reopen(self):
        self.root.wm_attributes("-alpha", 1.0)
 
class CreateAccountWindow:
    def __init__(self, welcome_window):
        self.welcome_window = welcome_window
        self.create_account = tk.Toplevel()
        self.create_account.title("Create Account")
        self.create_account.geometry("600x600")
        self.create_account.configure(bg="#071952")
        window_width = 800
        window_height = 600

        screen_width = self.create_account.winfo_screenwidth()
        screen_height = self.create_account.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.create_account.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.create_widgets()
        self.create_account.mainloop()

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
        name_label = tk.Label(self.create_account, text="Name:", fg="#37B7C3" , bg="#071952")
        name_label.place(relx=0.1, rely=0.1)
        self.name_entry = tk.Entry(self.create_account)
        self.name_entry.place(relx=0.3, rely=0.1)
 
        surname_label = tk.Label(self.create_account, text="Surname:", fg="#37B7C3" , bg="#071952")
        surname_label.place(relx=0.1, rely=0.15)
        self.surname_entry = tk.Entry(self.create_account)
        self.surname_entry.place(relx=0.3, rely=0.15)
 
        id_label = tk.Label(self.create_account, text="ID No.:", fg="#37B7C3" , bg="#071952")
        id_label.place(relx=0.1, rely=0.2)
        self.id_entry = tk.Entry(self.create_account)
        self.id_entry.place(relx=0.3, rely=0.2)
 
        phone_label = tk.Label(self.create_account, text="Phone:", fg="#37B7C3" , bg="#071952")
        phone_label.place(relx=0.1, rely=0.25)
        self.phone_entry = tk.Entry(self.create_account)
        self.phone_entry.place(relx=0.3, rely=0.25)
 
        email_label = tk.Label(self.create_account, text="Email:", fg="#37B7C3" , bg="#071952")
        email_label.place(relx=0.1, rely=0.3)
        self.email_entry = tk.Entry(self.create_account)
        self.email_entry.place(relx=0.3, rely=0.3)
        

        account_type_label = tk.Label(self.create_account, text="Account Type:", fg="#37B7C3" , bg="#071952")
        account_type_label.place(relx=0.1, rely=0.35)
        self.account_type = tk.StringVar(value="Cheque")
        cheque_radio = tk.Radiobutton(self.create_account, text="Cheque", variable=self.account_type, value="cheque",fg ="#37B7C3" , bg="#071952")
        cheque_radio.place(relx=0.3, rely=0.35)
        savings_radio = tk.Radiobutton(self.create_account, text="Savings", variable=self.account_type, value="savings", fg = "#37B7C3" , bg="#071952")
        savings_radio.place(relx=0.5, rely=0.35)


        balance_label = tk.Label(self.create_account, text="Opening Balance:", fg="#37B7C3" , bg="#071952")
        balance_label.place(relx=0.1, rely=0.4)
        self.balance_entry = tk.Entry(self.create_account)
        self.balance_entry.place(relx=0.3, rely=0.4)
 
        pin_label = tk.Label(self.create_account, text="Pin Number:", fg="#37B7C3" , bg="#071952")
        pin_label.place(relx=0.1, rely=0.45)
        self.pin_entry = tk.Entry(self.create_account, show="*")
        self.pin_entry.place(relx=0.3, rely=0.45)
 
        password_label = tk.Label(self.create_account, text="Password:", fg="#37B7C3" , bg="#071952")
        password_label.place(relx=0.1, rely=0.5)
        self.password_entry = tk.Entry(self.create_account)
        self.password_entry.place(relx=0.3, rely=0.5)
       
        generate_btn = tk.Button(self.create_account, text="Generate", command=self.generate_password, bg="#2196F3", fg="white", padx=1, pady=1)
        generate_btn.place(relx=0.6, rely=0.5)
 
        self.strength_label = tk.Label(self.create_account, text="Password Strength:",fg="#37B7C3" , bg="#071952")
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
        WelcomeWindow().__init__
         
        

    def go_back(self):
        self.create_account.destroy()
        WelcomeWindow().__init__
 
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
 
    #def create_account_function(self):
        #if self.validate_entries():
            #messagebox.showinfo("Success", "Account created successfully.")
       
class LoginWindow:
    def __init__(self, welcome_window):
        global recipient_name
        global accounts_file
        global banks_file
        global transaction_log

        
        
        accounts_file= "accounts.csv"
        banks_file= "banks.csv"
        transaction_log = "transactionslog.txt"
        self.welcome_window = welcome_window
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
        self.login.mainloop()
 
    def create_widgets(self):
        name_label = tk.Label(self.login, text="Name:", fg="#37B7C3" , bg="#071952")
        name_label.place(relx=0.1, rely=0.2)
        self.name_entry = tk.Entry(self.login)
        self.name_entry.place(relx=0.3, rely=0.2)
        recipient_name= self.name_entry
        
        email_label = tk.Label(self.login, text="Email:", fg="#37B7C3" , bg="#071952")
        email_label.place(relx=0.1, rely=0.3)
        self.email_entry = tk.Entry(self.login,width=30)
        self.email_entry.place(relx=0.3, rely=0.3)

        pin_label = tk.Label(self.login, text="Pin:", fg="#37B7C3" , bg="#071952")
        pin_label.place(relx=0.1, rely=0.4)
        self.pin_entry = tk.Entry(self.login, show="*")
        self.pin_entry.place(relx=0.3, rely=0.4)

        id_label = tk.Label(self.login, text="ID Number:", fg="#37B7C3" , bg="#071952")
        id_label.place(relx=0.1, rely=0.5)
        self.id_entry = tk.Entry(self.login)
        self.id_entry.place(relx=0.3, rely=0.5)

        login_btn = tk.Button(self.login, text="Login", command=self.login_function, bg="#4CAF50", fg="white", padx=20, pady=10)
        login_btn.place(relx=0.5, rely=0.7, anchor="center")

        forgot_pin_link = tk.Label(self.login, text="Forgot Pin?", fg="#EBF4F6" , bg="#071952", cursor="hand2")
        forgot_pin_link.place(relx=0.6, rely=0.4)
        forgot_pin_link.bind("<Button-1>", lambda event: self.forgot_pin())

        back_btn = tk.Button(self.login, text="Back", command=self.go_back, bg="#FF5722", fg="white", padx=20, pady=10)
        back_btn.place(relx=0.3, rely=0.7, anchor="center")

        self.login.protocol("WM_DELETE_WINDOW", self.on_close)
        self.login.mainloop()

    def on_close(self):
        self.login.destroy()
        WelcomeWindow()

    def go_back(self):
        self.login.destroy()
        WelcomeWindow()

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
                                bankswift.BankingApplicationGUI(recipient_name,accounts_file,banks_file,transaction_log)
                                return 
                        
                    messagebox.showerror("Error", "Invalid credentials. Please try again.")
            except FileNotFoundError:
                messagebox.showerror("Error", "Password records file not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

class DashboardWindow:
    global recipient_name
    
 
if __name__ == "__main__":
    WelcomeWindow()
 