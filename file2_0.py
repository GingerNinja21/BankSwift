import email
import os
import pandas as pd
import requests
import csv
import random
import re
from io import StringIO
import pandas as pd
from email_validator import validate_email


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
        self.invalid_username_id_pair = ""
        try:
            with open("userdata/accounts.csv", "r") as file:

                for line in file:
                    parts = line.strip().split(",")

                    if len(parts) < 7:
                        continue  
                    
                    stored_username = parts[1].strip().lower()
                    stored_usersurname = parts[2].strip().lower()
                    stored_account_type = parts[5].strip().lower()
                    stored_id = parts[6].strip().lower()
        
                        
                    if self.account_tally(self.account_type):
                        self.error_message = f"You already have existing accounts for the provided ID number!\nYou are only allowed to have 5 registered {self.account_type.capitalize()} accounts!\nRefer to Bankswifts User policy for more information."




                    if  (self.id_no.lower() == stored_id) and (not (self.Username.lower()== stored_username) or not(self.Usersurname.lower() == stored_usersurname)):
                        self.invalid_username_id_pair = f"\nThe ID number provided already exists in our database! \n{self.Username.capitalize()} {self.Usersurname.capitalize()} does not match the Name and Surname linked to the provided ID number in our database!"
                       
                       
                
                    if self.id_no.lower() == stored_id and self.Username.lower()== stored_username and self.Usersurname.lower() == stored_usersurname :
                        account_exists= True
                        self.existing_user_id_acc_creation_message ="\nAn account already exists for the provided ID number!\nWould you like to create a new account? "   

                    
                        if (self.Username.lower() == stored_username and 
                                self.Usersurname.lower() == stored_usersurname and 
                                self.account_type.lower() == stored_account_type and
                                self.id_no.lower() == stored_id):
                                account_exists= True

                        else:
                            self.existing_user_id_acc_creation_message ="\nAn account already exists for the provided ID number!\n""Would you like to create a new account? "   
                          
                                 
                return account_exists
        
            

        except FileNotFoundError:
            self.error_message += "\nError: Accounts file not found!"
            return self.error_message
        except Exception as e:
            self.error_message += f"Something went wrong! \nContact Administrator\n(Error location: account_existence, Error: {str(e)})"
            return self.error_message


    def account_tally(self,acc_type):
        try:
            self.acc_tally = 0
            with open("userdata/accounts.csv", "r") as file:

                for line in file:
                    parts = line.strip().split(",")

                    if self.id_no == parts[6]:
                        if acc_type.lower() == parts[5] :
                             self.acc_tally += 1
                        
                        

            
            if self.acc_tally >= 5:
                    return True
                    
            else:
                    return False
                         

        except:
             print()

         

    def valid_acc_no(self):  
        global stored_account_no
        global account_bank

        try :
             with open("userdata/accounts.csv", "r") as file:
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
        
        except :
                self.error_message += "\nInvalid Email"
                return False

    def bank(self):
        global account_bank
        try:
            with open("userdata/accounts.csv", "r") as file:
                    
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
            with open("userdata/accounts.csv", "r") as file:
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
    def __init__(self, email, id_no, pin):
        self.email = email.strip().lower()
        self.id_no = id_no.strip().lower()
        self.pin = pin.strip().lower()
        self.special_chars = ["-", "^", "'"]  
        self.error_message = ""
        
        self.validate_pin() 
        self.id_validation()
        self.validate_email()

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

    def validate_email(self):
        try:    
            valid = validate_email(self.email)
            email = valid.email
            return True
        
        except:
            self.error_message += "\nInvalid Email"
            return False

    def account_existence(self):
        account_exists = False
        try:
            with open("userdata/passwordrecords.csv", "r") as file:
                for line in file:
                    parts = line.strip().split(",")

                    if len(parts) < 6:
                        continue 

                    stored_id = parts[6].strip().lower()
                    stored_email = parts[3].strip().lower()
                    

                    if self.email == stored_email and self.id_no == stored_id:
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
        
   
class account_creation:

    def __init__(self, User_name, User_surname,id_no,pin, phone_number,password,email, balance,account_type):
        self.Username = User_name.strip().lower()
        self.Usersurname = User_surname.strip().lower()
        self.id_no = str(id_no.strip())
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

    def store_account(self):
        try:
            new_account_no = self.acc_no_generator()
            stored_data = []
            
            validator = DataValidation(self.Username,self.Usersurname,self.id_no,self.email,self.phone_number,self.pin,self.balance,self.account_type)
            df = pd.read_csv("userdata/accounts.csv")
            if validator.account_existence():
                Uid = validator.get_uid()
            else:
                Uid = df['uid'].max() + 1 if not df.empty else 0
            stored_data.append({"uid": Uid, "Name": self.Username, "Surname": self.Usersurname, "Account_no": new_account_no, "Balance": self.balance, "Account_type": self.account_type, "Id_no": self.id_no, "Linked_accounts": ""})

            file_name = "userdata/accounts.csv"
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
            with open("userdata/accounts.csv", "r") as file:
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
                        
            file_name = "userdata/passwordrecords.csv"
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



