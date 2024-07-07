import requests
import csv
import random
from io import StringIO


stored_account_no="151876453"
account_bank=" test"
### Initialization ###
class DataValidation:

    def __init__(self, User_name, User_surname,id_no):
        self.Username = User_name.strip()
        self.Usersurname = User_surname.strip()
        self.id_no = id_no.strip() 
        self.special_chars = ["-", "^" ,"\'"]  
        self.error_message = ""  

        
        self.validate_username()
        self.validate_usersurname()
    
    def validate_username(self):
        for char in self.Username:
            if not (char.isalpha() or char in self.special_chars):
                self.error_message += "\nPlease remove any special characters or numbers when entering your Name!"
                break

    def validate_usersurname(self):
        for char in self.Usersurname:
            if not (char.isalpha() or char in self.special_chars):
                self.error_message += "\nPlease remove any special characters or numbers when entering your Surname!"
                break

    def account_existence(self):
        global stored_username
        global stored_usersurname
        try:
            with open("accounts.csv", "r") as file:
                for line in file:
                    parts = line.strip().split(",")

                    stored_username = parts[1].strip().lower()
                    stored_usersurname = parts[2].strip().lower()
                    if self.Username.lower() == stored_username and self.Usersurname.lower() == stored_usersurname:
                        return True
                    
                self.error_message += "\nAccount does not Exist!"
                return False      

                      
                    
        except FileNotFoundError:
            self.error_message += "\nError: Accounts file not found!"
        except Exception as e:
            return f"\nError: {str(e)}"

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
                        break

                    elif not stored_account_no.isdigit():
                        self.error_message += "\nInvalid Account no! [Variable Type Error]"
                        
                        break

                    else:
                        return True
                            
        except:
                print("smth went wrong")

    def bank(self):
        global account_bank

        with open("accounts.csv", "r") as file:
                
                for line in file:
                    parts = line.strip().split(",")
                    print(stored_account_no,":",parts[3])

                    if stored_account_no[:3] == "151" :
                            account_bank = "Bankswift"
                            
                                
                    elif stored_account_no[:3] == "921" :
                            account_bank = "FNB"
       
                    
                    return account_bank

    def get_error_message(self):
    
       
        return self.error_message
                          
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
            self.error_message="Something went wrong! \nContact Administrator"

class account_creation:

    def __init__(self, User_name, User_surname,id_no):
        self.Username = User_name.strip().lower()
        self.Usersurname = User_surname.strip().lower()
        self.id_no = id_no.strip() 
        self.special_chars = ["-", "^" ,"\'"]  

        self.new_account = DataValidation(self.Username,self.Usersurname,self.id_no) 
        
       
        self.new_account.id_validation()
        self.new_account.account_existence()
        self.new_account.valid_acc_no()
        

    def password_generation(self):
        try:
            print("account existence:",self.new_account.account_existence())
            if self.new_account.account_existence() == True:
               self.new_account.error_message += "\nAccount already exists!"

               
            
            else:

                password = ""
                ascii_characters = [
                    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>',
                    '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\',
                    ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    '{', '|', '}', '~'
                ]
                


                while len(password) <= 11:
                    password += random.choice(ascii_characters)
                    

                    ### Storing Passwords ##
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
        except:
               print()
               
                    # return x

    # def acc_no_generator(acc_type):
    #     valid_char= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]
    #     acc_type=""
    #     gen_acc_no = ""

    #     while len(gen_acc_no) != 9 :
    



### Testing area ###
username="john"
usersurname= "doe"
id_no="0214536215243"
x= account_creation(username,usersurname,id_no)
y= x.password_generation()
z= x.new_account
r= DataValidation(username,usersurname,id_no)
c= r.get_error_message()
print("c:",c)
print*(error_message)
# r= x.valid_acc_no()
# z=x.get_error_message()
# # t= x.bank()
# print("\nAccount existence:",y ,"\n error message:",z ,"\nValid account no:",r ,"\n", t )

