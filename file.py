import requests
import csv
import random
from io import StringIO



### Initialization ###
class DataValidation:

    def __init__(self, User_name, User_surname,id_no):
        self.Username = User_name.strip()
        self.Usersurname = User_surname.strip()
        self.id_no = id_no.strip() 
        self.special_chars = ["-", "^"]  
        self.error_message = ""  
        print(self.Username , self.Usersurname)
        
        # Validate inputs during initialization
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
        try:
            with open("accounts.csv", "r") as file:
                for line in file:
                    print(line)
                    if self.Username.lower() in line :
                        return True
                    
                self.error_message += "\nAccount does not Exist!"
                return False      
                       
                    
        except FileNotFoundError:
            self.error_message += "\nError: Accounts file not found!"
        except Exception as e:
            return f"\nError: {str(e)}"
        

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

### Testing area ###
username="samantha"
usersurname= "laqua"
id_no="0214536215243"
x= DataValidation(username , usersurname, id_no)
y= x.account_existence()
r= x.id_validation()
z=x.get_error_message()
print("\nAccount existence:",y ,"\n error message:",z ,"\nValid ID:",r)

