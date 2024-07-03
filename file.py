import requests
import csv
import random
from io import StringIO


### Initialization ###
class DataValidation:
   
    def __init__(self,User_name , User_surname):
     
     global Username
     global Usersurname
     global special_char
     global error_message
     

     Username = User_name.strip()
     Usersurname = User_surname.strip()
     error_message=""
     special_char= ["-" ,"^"]
    

     for char in Username:
        if not (char.isalpha() or char in special_char):
            error_message = "\nPlease remove any Special Characters or Numbers when entering your details!"
            break
   
    def get_error_message(self):
        return error_message
    
    def Account_existence(self):
        Existence = False

        try:

            with open("accounts.csv") as x:
                file = x.readlines()
                for line in file :
                    if  Username.lower() in line and Usersurname.lower() in line : 
                        Existence = True
                        break
                
                if not Existence:
                    error_message= "\nAccount does not exist or Incorrect Credentials. \nCheck the spelling and try again."
                    return error_message
                    
                else:
                    return Existence

            
        except (ValueError, AttributeError, TypeError ):
            error_message="\nAccount does not exist or Incorrect Credentials. \nCheck the spelling and try again."
            return error_message

        except:
             error_message="Something went wrong. Contact Administration!"
             return error_message
        

def password_generation(name):
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
    stored_passwords.append({"Name" : name , "Password" : password})

    file_name = "password_records.csv"
    fields= ["Name" , "Password"]

    with open(file_name , "a" , newline="") as csvfile:
        scribe = csv.DictWriter(csvfile , fieldnames = fields )
        
        ### Checks if file is empty ###
        if csvfile.tell () == 0:
            scribe.writeheader()

        scribe.writerows(stored_passwords)

    return password



class Accounts():

    def __init__(self,UID):
        self.UserID = UID

    def acc_no_generator(UID):
        unique_no = True
        with open("accounts.csv") as x:
            file = x.readlines()
            for line in file:
                if UID in line :
                    current_line = line
                    selected_line = current_line.split(sep=",") 
                    if len(selected_line) >= 0:
                        account_no = selected_line[3]
                        if account_no == "" :
                            account_no = random.randint(100000000, 999999999)
                            





### Testing area ###
x= DataValidation.__init__("","john" ,"doe")
y= DataValidation.Account_existence(self=DataValidation)
z=DataValidation.get_error_message(self=DataValidation)
v= Accounts.acc_no_generator("0001")
# print("Init:", x ,"\nAccount existence:",y ,"\n error message",z)

