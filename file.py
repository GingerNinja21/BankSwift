import pandas as pd
import requests
import csv
import random
import re
from io import StringIO
import pandas as pd
from email_validator import validate_email, EmailNotValidError


stored_account_no=""
account_bank=""
### Initialization ###
class DataValidation:

    def __init__(self, User_name, User_surname,id_no,email,phone_number,pin ,balance, account_type):
        self.Username = User_name.strip()
        self.Usersurname = User_surname.strip()
        self.id_no = id_no.strip()
        self.pin= pin.strip()
        self.phone_number= phone_number.strip()
        self.email = email.strip()
        self.balance = balance.strip()
        self.account_type = account_type.strip().lower()
        self.special_chars = ["-", "^" ,"\'"]  
        self.error_message = ""  
        self.existing_user_account = False
        self.existing_user_id_acc_creation_message = ""
        self.invalid_username_id_pair = ""


        
        self.validate_username_and_surname()
        self.id_validation()
        self.validate_phone_number()
        self.validate_email()
        self.validate_pin()
        self.validate_opening_balance()
            
    def validate_username_and_surname(self):
        for char in self.Username:
            if not (char.isalpha() or char in self.special_chars):
                self.error_message += "\nPlease remove any special characters or numbers when entering your Name and Surname!"
                return
        
        for char in self.Usersurname:
            if not (char.isalpha() or char in self.special_chars):
                self.error_message += "\nPlease remove any special characters or numbers when entering your Name and Surname!"
                return
            
    def account_existence(self):
        account_exists = False
        self.existing_user_id_acc_creation_message =""
        self.invalid_username_id_pair = ""
        try:
            with open("accounts.csv", "r") as file:
                for line in file:
                    parts = line.strip().split(",")

                    if len(parts) < 7:
                        continue  

                    stored_username = parts[1].strip().lower()
                    stored_usersurname = parts[2].strip().lower()
                    stored_account_type = parts[5].strip().lower()
                    stored_id = parts[6].strip().lower()


                    if  (self.id_no.lower() == stored_id) and (not (self.Username.lower()== stored_username) or not(self.Usersurname.lower() == stored_usersurname)):
                        self.invalid_username_id_pair = f"\nThe ID number provided already exists in our database! \n{self.Username} and {self.Usersurname} does not match the Name and Surname linked to the provided ID number in our database!"
                       

                    if self.id_no.lower() == stored_id and self.Username.lower()== stored_username and self.Usersurname.lower() == stored_usersurname :
                        account_exists= True
                        self.existing_user_id_acc_creation_message ="\nAn account already exists for the provided ID number!\n""Would you like to create a new account? "   

                    
                return account_exists
            

        except FileNotFoundError:
            self.error_message += "\nError: Accounts file not found!"
            return self.error_message
        except Exception as e:
            self.error_message += f"Something went wrong! \nContact Administrator\n(Error location: account_existence, Error: {str(e)})"
            return self.error_message


    def valid_acc_no(self):  
        global stored_account_no
        global account_bank

        try :
             with open("accounts.csv", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    
                    if self.Username.lower() == parts[1] and self.Usersurname.lower() == parts[2]:
                        stored_account_no = parts[3].strip()
                        self.error_message += "Account already exists!"
                        return False
                        break

                    elif  len(stored_account_no) != 9:
                            self.error_message += "\nInvalid Account no! [too many char's]"
                            return False    


                    elif not stored_account_no.isdigit():
                        self.error_message += "\nInvalid Account no! [Variable Type Error]"
                        
                        break

                    else:
                        return True
                            
        except:
                self.error_message+="Something went wrong! \nContact Administrator\n(Error location: valid_acc_no)"

    def validate_pin(self):
        try:       
            if len(self.pin) != 5 :
                 self.error_message += "\nPin does not meet the minimum requirements!\nYour pin needs to contain 5 digits!"
                 return False    
            
            if not(self.pin.isdigit()):
                 self.error_message += "\nPin does not meet the minimum requirements!\nYour cannot contain Letters or Special characters!"
                 return False
            else:
                 return True
        except: 
                self.error_message+="Something went wrong! \nContact Administrator\n(Error location: validate_pin)"

    def validate_phone_number(self):
        regex = r'^(\+27|0)\d{9}$'
        if re.match(regex, self.phone_number):
            return True
        else:
            self.error_message +="\nInvalid phone number!"
            return False

    def validate_email(self):
        try:    
                valid = validate_email(self.email)
                email = valid.email
                return True
        
        except EmailNotValidError as e:
                self.error_message += "\n" + str((e))
                return False

    def bank(self):
        global account_bank
        try:
            with open("accounts.csv", "r") as file:
                    
                    for line in file:
                        parts = line.strip().split(",")

                        if stored_account_no[:3] == "151" :
                                account_bank = "Bankswift"

                        elif stored_account_no[:1] == "4" :
                                if stored_account_no[:3] =="470" or stored_account_no[:4] =="4700":
                                    account_bank = "Capitec"
                                else:
                                    account_bank = "ABSA"       
                                    
                        elif stored_account_no[:1] == "6" :
                                account_bank = "FNB"
                        
                        elif stored_account_no[:1] == "1" or "0" :
                                if stored_account_no[:2] == "15":
                                    account_bank = "Nedbank"
                                else: 
                                    account_bank = "Standard Bank"
            
                        
                        elif stored_account_no[:1] == "5" or "2" :
                                account_bank = "Nedbank"
                    return account_bank
        except:
                self.error_message+="Something went wrong! \nContact Administrator\n(Error location: bank() function)"

    def get_error_message(self):
        error_message= self.error_message
        return error_message

    def get_uid(self):
        try:
            uid = ""
            with open("accounts.csv", "r") as file:
                for line in file:
                    parts = line.strip().split(",")

                    stored_username = parts[1]
                    stored_usersurname = parts[2]
                    stored_id = parts[6].strip().lower()
                    if self.id_no == stored_id and self.Username.lower() == stored_username and self.Usersurname.lower() == stored_usersurname:
                        uid = parts[0]
                        return uid
                


        except:
             self.error_message += f"Something went wrong! \nContact Administrator\n(Error location: get_uid)"

    def id_validation(self):
        try:
            if len(self.id_no) != 13 :
                self.error_message += "\nInvalid ID number!"
                return False
            
            elif not self.id_no.isdigit():
                self.error_message += "\nInvalid ID number! Remove any characters that are not Numbers!"
                return False
            
            else :
                return True
        except:
            self.error_message+="Something went wrong! \nContact Administrator\n(Error location: id_validation)"

    def validate_opening_balance(self):
            
            try:
                opening_balance = self.balance
                amount = int(opening_balance)
                if not (amount) or not (amount>= 100) :
                    self.error_message += "\nInsufficient opening balance!\nMinimum amount: R100"
                    return False
                else:
                    return True
            
            except:
                self.error_message += "\nSomething went wrong! \nContact Administrator\n(Error location: validate_opening_balance)"

class LoginValidation:
    def __init__(self, username, id_no, pin):
        self.username = username.strip().lower()
        self.id_no = id_no.strip().lower()
        self.pin = pin.strip().lower()
        self.special_chars = ["-", "^", "'"]  
        self.error_message = ""
        
        self.validate_username()
        self.validate_pin() 
        self.id_validation()

    def validate_pin(self):
        try:       
            if len(self.pin) != 5:
                self.error_message += "\nPin does not meet the minimum requirements!\nYour pin needs to contain 5 digits!"
                return False    
            
            if not self.pin.isdigit():
                self.error_message += "\nPin does not meet the minimum requirements!\nYour pin cannot contain letters or special characters!"
                return False
            return True
        except Exception as e: 
            self.error_message += f"Something went wrong! \nContact Administrator\n(Error location: validate_pin)\n{str(e)}"
            return False
    
    def id_validation(self):
        try:
            if len(self.id_no) != 13:
                self.error_message += "\nInvalid ID number!"
                return False
            
            if not self.id_no.isdigit():
                self.error_message += "\nInvalid ID number! Remove any characters that are not numbers!"
                return False
            return True
        except Exception as e:
            self.error_message += f"Something went wrong! \nContact Administrator\n(Error location: id_validation)\n{str(e)}"
            return False

    def validate_username(self):
        try:
            for char in self.username:
                if not (char.isalpha() or char in self.special_chars):
                    self.error_message += "\nPlease remove any special characters or numbers when entering your Name and Surname!"
                    return False
            return True
        except Exception as e:
            self.error_message += f"Something went wrong! \nContact Administrator\n(Error location: validate_username)\n{str(e)}"
            return False
     
    def account_existence(self):
        account_exists = False
        try:
            with open("accounts.csv", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    

                    if len(parts) < 7:
                        continue  # Skip 

                    stored_id = parts[6].strip().lower()
                    stored_name = parts[1].strip().lower()

                    if self.id_no == stored_id and self.username == stored_name:
                        account_exists = True
                        break

            if not account_exists:
                self.error_message += "\nAccount does not exist!"  
            return account_exists
        

        except FileNotFoundError:
            self.error_message += "\nError: Accounts file not found!"
        except Exception as e:
            self.error_message += f"Something went wrong! \nContact Administrator\n(Error location: account_existence)\n{str(e)}"
            return False


    def password_recovery(self):
        try:
            with open("password_records.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if (self.Username.lower() == row['name'].lower() and 
                        self.Usersurname.lower() == row['surname'].lower() and
                        self.id_no == row['id']):
                        return f"Your password is: {row['password']}"
                
            return "Password not found. Please check your details and try again."
        
        except FileNotFoundError:
            return "Password records file not found."
        except Exception as e:
            return f"Error retrieving password: {str(e)}"
        
class account_creation:

    def __init__(self, User_name, User_surname,id_no,pin, phone_number,password,email, balance,account_type):
        self.Username = User_name.strip().lower()
        self.Usersurname = User_surname.strip().lower()
        self.id_no = id_no.strip() 
        self.pin= pin.strip()
        self.password= password.strip()
        self.email= email.strip()
        self.balance= balance.strip()
        self.account_type= account_type.strip().lower()
        self.phone_number = phone_number.strip()

        self.special_chars = ["-", "^" ,"\'"]  
        self.error_message = ""  
    
    
        
    def get_error_message(self):
        x= self.error_message
        return x
    
    # def password_generation(self):
        try:
            if existing_account == True:
               self.error_message += "\nAccount already exists!" 

            elif valid_id == False:
                  self.error_message+=""

            else:        
                password = ""
                ascii_characters = [
                    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>',
                    '?', '@', 'A', 'BF', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\',
                    ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    '{', '|', '}', '~'
                ]
                


                while len(password) <= 11:
                    password += random.choice(ascii_characters)
                    

                    ## Storing Passwords ##
                stored_passwords=[]
                stored_passwords.append({"Name" : self.Username ,"Surname" : self.Usersurname ,"Password" : password})
                    
                file_name = "password_records.csv"
                fields= ["Name" ,"Surname", "Password"]
                    
                with open(file_name , "a" , newline="") as csvfile:
                    scribe = csv.DictWriter(csvfile , fieldnames = fields )
                    ## Checks if file is empty ###
                    if csvfile.tell () == 0:
                        scribe.writeheader()
                    
                    scribe.writerows(stored_passwords)
                    
                
                return password
        except Exception as e:
                self.error_message += "\nSomthing went wrong! Contact Administrator!\n(Error location: password_generation)"  

    def store_account(self):
        try:
            new_account_no = self.acc_no_generator()
            stored_data = []
            
            validator = DataValidation(self.Username,self.Usersurname,self.id_no,self.email,self.phone_number,self.pin,self.balance,self.account_type)
            df = pd.read_csv("accounts.csv")
            if validator.account_existence():
                Uid = validator.get_uid()
            else:
                Uid = df['uid'].max() + 1 if not df.empty else 0
            stored_data.append({"uid": Uid, "Name": self.Username, "Surname": self.Usersurname, "Account_no": new_account_no, "Balance": self.balance, "Account_type": self.account_type, "Id_no": self.id_no, "Linked_accounts": ""})

            file_name = "accounts.csv"
            fields = ["uid", "Name", "Surname", "Account_no", "Balance", "Account_type", "Id_no", "Linked_accounts"]

            with open(file_name, "a", newline="") as csvfile:
                scribe = csv.DictWriter(csvfile, fieldnames=fields)
                if csvfile.tell() == 0:
                    scribe.writeheader()
                scribe.writerows(stored_data)
            return "Account saved successfully!"
        except Exception as e:
            return f"Something went wrong! Contact Administrator!\n(Error location: store_account)\n{str(e)}"
           
    def acc_no_generator(self):
        valid_char= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]

        gen_acc_no = "151"
        valid_acc = False
        try:
            while len(gen_acc_no) != 9 :
                    gen_acc_no += random.choice(valid_char)
            stored_account_no = gen_acc_no
            with open("accounts.csv", "r") as file:
                while valid_acc == False:    
                    for line in file:
                        parts = line.strip().split(",")
                        if stored_account_no == parts[3]:
                            continue
                        else:
                            valid_acc = True 
                            return gen_acc_no
            
                            
    
        except:
             self.error_message += "\nSomething went wrong! Contact Administration!\n(Error location: acc_no_generator)"

    def store_passwords(self):
        try:
            stored_passwords=[]
            stored_passwords.append({"Name" : self.Username ,"Surname" : self.Usersurname ,"id":self.id_no ,"email":self.email ,"Password" : self.password ,"Pin":self.pin})
                        
            file_name = "password_records.csv"
            fields= ["Name" ,"Surname","id","email", "Password","Pin"]
                        
            with open(file_name , "a" , newline="") as csvfile:
                    scribe = csv.DictWriter(csvfile , fieldnames = fields )
                        ## Checks if file is empty ###
                    if csvfile.tell () == 0:
                        scribe.writeheader()
                        
                    scribe.writerows(stored_passwords)
                    return 
        
        except:
                self.error_message += "\nSomthing went wrong! Contact Administrator!\n(Error location: store_account)"  

   
         
### Testing area ###
# username="john"
# usersurname= "doe"
# id_no="0214536241543"


# ac = account_creation(username, usersurname, id_no,"0210085197080","0840523857","asdfqwertyui","test@gmail.com","500","cheque")
# result = ac.store_account(username, usersurname, id_no, acc_type)
# print(result)
# x= ac.acc_no_generator()
# print(x)

