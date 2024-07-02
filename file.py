import csv
import random


### Initialization ###
class DataValidation:
    def __init__(self, User_name , User_surname):
        self.Name = User_name
        self.Surname = User_surname
        
        
    def Account_existence(self):
        Existence = False
        try:
            with open("password_records.csv") as x:
                file = x.readlines()
                for line in file :
                    if  User_name
        except:
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



