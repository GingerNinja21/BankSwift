import datetime
import pandas as pd
from file import DataValidation,account_creation

class BankingApplication:
    def __init__(self, recipient_name):
        self.recipient_name = recipient_name
        self.accounts_file = "accounts.csv"
        self.banks_file = "banks.csv"
        self.transactions_log = "transactionslog.txt"
        self.account_type = self.get_account_type(recipient_name)
        
    # def __init__(self, accounts_file):
    #     self.accounts_file = accounts_file

    # def account_exists(self, account_name):
    #     df = pd.read_csv(self.accounts_file)
    #     account_exists = not df[df['name'].str.lower() == account_name.lower()].empty
    #     return account_exists

    def create_new_account(self, username, usersurname, id_no, acc_type):
        # account_creation - create a new account
        creation = account_creation(username, usersurname, id_no, acc_type)
        if creation.get_error_message():
            error_message = creation.get_error_message()
            print(error_message)
        else:
            new_account_no = creation.acc_no_generator()
            if new_account_no:
                print(f"New account created with account number: {new_account_no}")
    #file.py
    def validate_user_input(self, username, usersurname, id_no):
        # Data Validation - validate user input
        validation = DataValidation(username, usersurname, id_no)
        if not validation.account_existence():
            error_message = validation.get_error_message()
            print(error_message)
            return False
        elif not validation.valid_acc_no():
            error_message = validation.get_error_message()
            print(error_message)
            return False
        elif not validation.id_validation():
            error_message = validation.get_error_message()
            print(error_message)
            return False
        else:
            return True

    def get_input(self, prompt):
        return input(prompt).strip()

    def get_account_type(self, account_name):
        df = pd.read_csv(self.accounts_file)
        account = df[df['name'].str.lower() == account_name.lower()]
        
        if not account.empty:
            return account['account_type'].values[0]
        else:
            print(f"Account '{account_name}' not found. Creating new account...")

            new_account_id = self.get_input("Enter your ID number: ")
            acc_type = self.get_input("Enter account type (Savings/Cheque): ")

            # Initialize account creation process
            new_account = account_creation(
                User_name=account_name,
                User_surname="unknown",  
                id_no=new_account_id,
                acc_type=acc_type
            )

            existing_account = new_account.new_account.account_existence()

            if not existing_account:
                # Generate new account number
                new_account_no = new_account.acc_no_generator()

                new_account_data = {
                    'uid': [df['uid'].max() + 1 if not df.empty else 0],
                    'name': [account_name],
                    'surname': ['unknown'],  
                    'account_no': [new_account_no],
                    'balance': [100],  
                    'account_type': [acc_type],
                    'id_number': [new_account_id],
                    'linked_accounts': ['']  
                }

                new_account_data_df = pd.DataFrame(new_account_data)

                # Append new account data to existing DataFrame
                df = pd.concat([df, new_account_data_df], ignore_index=True)
                df.to_csv(self.accounts_file, index=False)
                
                print(f"New account created for {account_name} with account number {new_account_no}, account type {acc_type}.")

            return acc_type

    def write_transaction(self, transaction_type, amount, to_account=None, to_account_name=None):
        transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        from_account_name = self.recipient_name
        if to_account and to_account_name:
            transaction_details = f"{transaction_time} - {transaction_type}: R{amount:.2f} - From: {from_account_name} - To: {to_account_name} ({to_account})\n"
        else:
            transaction_details = f"{transaction_time} - {transaction_type}: R{amount:.2f} - From: {from_account_name}\n"
        
        with open(self.transactions_log, "a") as file:
            file.write(transaction_details)

    def update_balance(self, amount):
        df = pd.read_csv(self.accounts_file)
        mask = df['name'].str.lower() == self.recipient_name.lower()
        if mask.any():
            df.loc[mask, 'balance'].astype(int) + int(amount)
            df.to_csv(self.accounts_file, index=False)
        else:
            print(f"Account '{self.recipient_name}' not found.")

    def withdraw(self):
        try:
            amount = float(self.get_input("Enter amount to withdraw: "))
            df = pd.read_csv(self.accounts_file)
            account = df[df['name'].str.lower() == self.recipient_name.lower()]
            if account.empty:
                print(f"Account '{self.recipient_name}' not found.")
                return
            balance = account['balance'].values[0]
            if amount <= 0:
                print("Amount must be greater than zero.")
            elif amount > balance:
                print("Insufficient funds.")
            else:
                self.update_balance(-amount)
                self.write_transaction("Withdraw", amount)
                print(f'R{amount:.2f} successfully withdrawn.')
        except ValueError:
            print("Please enter a valid number.")

    def show_available_accounts(self):
        print("Available accounts:")
        df = pd.read_csv(self.accounts_file)
        for _, row in df.iterrows():
            print(f"{row['uid']} - {row['name']} , acc_no: {row['account_no']}")

    def transfer(self):
        self.show_available_accounts()
        try:
            recipient_name = self.get_input("Enter recipient account name: ")
            df = pd.read_csv(self.accounts_file)
            recipient_account = df[df['name'].str.lower() == recipient_name.lower()]
            if recipient_account.empty:
                create_new = self.get_input("Account not found. Do you want to create a new account? (yes/no): ").lower()
                if create_new == 'yes':
                    recipient_account_no = self.get_input("Enter new account number for recipient: ")
                    new_account_uid = df['uid'].max() + 1 if not df.empty else 0
                    new_account = pd.DataFrame([{
                        'uid': new_account_uid, 
                        'name': recipient_name, 
                        'surname': 'unknown', 
                        'account_no': recipient_account_no, 
                        'balance': 100, 
                        'account_type': '', 
                        'id_number': "",
                        'linked_accounts': ""
                    }])
                    df = pd.concat([df, new_account], ignore_index=True)
                    df.to_csv(self.accounts_file, index=False)

                    df_banks = pd.read_csv(self.banks_file)
                    new_bank_account = pd.DataFrame([{
                        'uid': new_account_uid, 
                        'name': recipient_name, 
                        'id_number': "",  
                        'bank_name': '',  
                        'account_no': recipient_account_no,
                        'linked_accounts': ""
                    }])
                    df_banks = pd.concat([df_banks, new_bank_account], ignore_index=True)
                    df_banks.to_csv(self.banks_file, index=False)

                    print(f'New account created for {recipient_name} with account number {recipient_account_no}')
                else:
                    print("Transfer cancelled.")
                    return
            else:
                recipient_account_no = recipient_account['account_no'].values[0]
            amount = float(self.get_input("Enter amount to transfer: "))
            sender_account = df[df['name'].str.lower() == self.recipient_name.lower()]
            if sender_account.empty:
                print(f"Account '{self.recipient_name}' not found.")
                return
            balance = sender_account['balance'].values[0]
            if amount <= 0:
                print("Amount must be greater than zero.")
            elif amount > balance:
                print("Insufficient funds.")
            else:
                self.update_balance(-amount)
                self.write_transaction("Transfer", amount, recipient_account_no, recipient_name)
                self.update_balance_recipient(amount, recipient_name)
                print(f'R{amount:.2f} successfully transferred to {recipient_name}')
        except ValueError:
            print("Please enter a valid number.")

    def update_balance_recipient(self, amount, recipient_name):
        df = pd.read_csv(self.accounts_file)
        mask = df['name'].str.lower() == recipient_name.lower()
        if mask.any():
            df.loc[mask, 'balance'] += amount
            df.to_csv(self.accounts_file, index=False)
        else:
            print(f"Recipient account '{recipient_name}' not found.")

    def view_balance(self):
        df = pd.read_csv(self.accounts_file)
        account = df[df['name'].str.lower() == self.recipient_name.lower()]
        if not account.empty:
            print(f"Your current balance is: R{account['balance'].values[0]:.2f}")
        else:
            print(f"Account '{self.recipient_name}' not found.")

    def manage_accounts(self):
        print("1 - Link New Account")
        print("2 - View Linked Accounts")
        print("3 - View Your Account Details")

        option = self.get_input("Please choose an option: ").strip()
        if option == '1':
            self.link_new_account()
        elif option == '2':
            self.view_linked_accounts()
        elif option == '3':
            self.view_account_details()
        else:
            print("Invalid option selected.")
            
    def link_new_account(self):
        account_to_link = self.get_input("Enter the name of the account to link: ").strip()
        df_banks = pd.read_csv(self.banks_file)

        df_banks['uid'] = pd.to_numeric(df_banks['uid'], errors='coerce').fillna(0).astype(int)

        mask = df_banks['name'].str.lower() == account_to_link.lower()
        if mask.any():
            index = df_banks.index[mask].tolist()[0]
            linked_accounts = df_banks.at[index, 'linked_accounts']
            if pd.isna(linked_accounts):
                linked_accounts = ""
            linked_accounts_list = linked_accounts.split(",") if linked_accounts else []
            if self.recipient_name not in linked_accounts_list:
                linked_accounts_list.append(self.recipient_name)
                df_banks.at[index, 'linked_accounts'] = ",".join(linked_accounts_list)
                df_banks.to_csv(self.banks_file, index=False)
                print(f"Account '{self.recipient_name}' successfully linked to '{account_to_link}'.")
            else:
                print(f"Account '{self.recipient_name}' is already linked to '{account_to_link}'.")
        else:
            print(f"Account '{account_to_link}' not found in banks. Creating a new account.")
            new_account_no = self.get_input("Enter new account number: ")
            new_bank_name = self.get_input("Enter bank name: ")
            new_account_uid = df_banks['uid'].max() + 1 if not df_banks.empty else 0
            new_account_id = self.get_input("Enter your ID number: ")

            new_account = pd.DataFrame([{
                'uid': new_account_uid,
                'name': account_to_link,
                'id_number': new_account_id,
                'bank_name': new_bank_name,
                'account_no': new_account_no,
                'linked_accounts': self.recipient_name
            }])
            df_banks = pd.concat([df_banks, new_account], ignore_index=True)
            df_banks.to_csv(self.banks_file, index=False)
            print(f"New bank account created for {account_to_link} and linked to '{self.recipient_name}'.")

    def view_linked_accounts(self):
        df_banks = pd.read_csv(self.banks_file)
        mask = df_banks['name'].str.lower() == self.recipient_name.lower()
        if mask.any():
            linked_accounts = df_banks[mask]['linked_accounts'].values[0]
            if linked_accounts:
                print(f"Linked accounts: {linked_accounts}")
            else:
                print("No linked accounts found.")
        else:
            print(f"Account '{self.recipient_name}' not found in banks.")

    def view_account_details(self):
        df = pd.read_csv(self.accounts_file)
        mask = df['name'].str.lower() == self.recipient_name.lower()
        if mask.any():
            account_details = df[mask].drop(columns=['uid', 'linked_accounts'])
            print(account_details.to_string(index=False))
        else:
            print(f"Account '{self.recipient_name}' not found.")

if __name__ == "__main__":
    recipient_name = input("Enter your account name: ").strip()
    app = BankingApplication(recipient_name)
    options = {
        '1': app.view_balance,
        '2': app.withdraw,
        '3': app.transfer,
        '4': app.manage_accounts
    }
    
    while True:
        print(" 1 - View Balance\n 2 - Withdraw\n 3 - Transfer\n 4 - Manage Accounts\n 5 - Exit")
        option = input("Please choose an option: ").strip()
        if option == '5':
            print("Thank you for using BankSwift. Goodbye!")
            break
        elif option in options:
            options[option]()
        else:
            print("Invalid option selected.")

