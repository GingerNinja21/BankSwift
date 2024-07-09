import datetime
import pandas as pd

recipient_name = input("Enter your account name: ")

def write_transaction(transaction_type, amount, account_type, account_name, to_account=None):
    transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if to_account:
        from_account_name = get_account_name(account_name)
        to_account_name = get_account_name(to_account)
        transaction_details = f"{transaction_time} - {transaction_type}: R{amount:.2f} - From: {from_account_name} ({account_type}) - To: {to_account_name}\n"
    else:
        from_account_name = get_account_name(account_name)
        transaction_details = f"{transaction_time} - {transaction_type}: R{amount:.2f} - From: {from_account_name} ({account_type})\n"

    with open("transactionslog.txt", "a") as file:
        file.write(transaction_details)

def get_input(prompt):
    return input(prompt).strip()

def get_account_name(account_number):
    df = pd.read_csv("accounts.csv")
    account = df[df['account_no'] == account_number]
    if not account.empty:
        return account['name'].values[0]
    return recipient_name

def get_account_type(account_name): 
    df = pd.read_csv("accounts.csv")
    account = df[df['name'].str.lower() == account_name.lower()]
    if not account.empty:
        account_type = account['account_type'].values[0]
        print(f"Using saved account type: {account_type}")
        return account_type
    else:
        print(f"Account '{account_name}' not found.")
        print("Creating new account...")
        new_account_no = get_input("Enter new account number: ")
        new_account_type = get_input("Enter account type (Savings/Cheque): ")
        new_account_uid = df['uid'].max() + 1 if not df.empty else 0
        new_account_id = get_input("Enter your ID number: ")
        
        # Add the new account to accounts.csv
        new_account = pd.DataFrame([{
            'uid': new_account_uid, 
            'name': account_name, 
            'surname': 'unknown', 
            'account_no': new_account_no, 
            'balance': 0.0, 
            'account_type': new_account_type,
            'id_number': new_account_id,
            'linked_accounts': ""
        }])
        df = pd.concat([df, new_account], ignore_index=True)
        df.to_csv("accounts.csv", index=False)
        
        # Adding the new account to banks.csv
        df_banks = pd.read_csv("banks.csv")
        new_bank_account = pd.DataFrame([{
            'uid': new_account_uid, 
            'name': account_name, 
            'id_number': new_account_id,
            'bank_name': 'FNB', 
            'account_no': new_account_no,
            'linked_accounts': ""
        }])
        df_banks = pd.concat([df_banks, new_bank_account], ignore_index=True)
        df_banks.to_csv("banks.csv", index=False)
        
        print(f"New account created for {account_name} with account number {new_account_no} and account type {new_account_type}.")
        return new_account_type

account_type = get_account_type(recipient_name)

def withdraw():
    try:
        withdraw_no = float(get_input("Enter amount to withdraw: "))
        
        df = pd.read_csv("accounts.csv")
        account = df[df['name'].str.lower() == recipient_name.lower()]
        
        if account.empty:
            print(f"Account '{recipient_name}' not found.")
            return

        balance = account['balance'].values[0]

        if withdraw_no <= 0:
            print("Amount must be greater than zero.")
        elif withdraw_no > balance:
            print("Insufficient funds.")
        else:
            update_balance(-withdraw_no)
            write_transaction("Withdraw", withdraw_no, account_type, recipient_name)
            print(f'R{withdraw_no:.2f} successfully withdrawn.')
    except ValueError:
        print("Please enter a valid number.")

def show_available_accounts():
    print("Available accounts:")
    df = pd.read_csv("accounts.csv")
    for _, row in df.iterrows():
        print(f"Recipient: {row['name']}, Account_no: {row['account_no']}")

def transfer():
    show_available_accounts()

    try:
        recipient_name_transfer = get_input("Enter recipient account name: ")

        df = pd.read_csv("accounts.csv")
        account = df[df['name'].str.lower() == recipient_name_transfer.lower()]

        if account.empty:
            create_new = get_input("Account not found. Do you want to create a new account? (yes/no): ").lower()
            if create_new == 'yes':
                recipient_account_no = get_input("Enter new account number for recipient: ")
                new_account_uid = df['uid'].max() + 1

                # Create new account in accounts.csv
                new_account = pd.DataFrame([{
                    'uid': new_account_uid, 
                    'name': recipient_name_transfer, 
                    'surname': 'unknown', 
                    'account_no': recipient_account_no, 
                    'balance': 0.0, 
                    'account_type': '', 
                    'id_number': "",
                    'linked_accounts': ""
                }])
                df = pd.concat([df, new_account], ignore_index=True)
                df.to_csv("accounts.csv", index=False)
                
                # Create new account in banks.csv
                df_banks = pd.read_csv("banks.csv")
                new_bank_account = pd.DataFrame([{
                    'uid': new_account_uid, 
                    'name': recipient_name_transfer, 
                    'id_number': "",  
                    'bank_name': '',  
                    'account_no': recipient_account_no,
                    'linked_accounts': ""
                }])
                df_banks = pd.concat([df_banks, new_bank_account], ignore_index=True)
                df_banks.to_csv("banks.csv", index=False)

                print(f'New account created for {recipient_name_transfer} with account number {recipient_account_no}')
            else:
                print("Transfer cancelled.")
                return
        else:
            recipient_account_no = account['account_no'].values[0]

        transfer_no = float(get_input("Enter amount to transfer: "))
        
        sender_account = df[df['name'].str.lower() == recipient_name.lower()]
        if sender_account.empty:
            print(f"Account '{recipient_name}' not found.")
            return
        
        balance = sender_account['balance'].values[0]
        
        if transfer_no <= 0:
            print("Amount must be greater than zero.")
        elif transfer_no > balance:
            print("Insufficient funds.")
        else:
            update_balance(-transfer_no)
            write_transaction("Transfer", transfer_no, account_type, recipient_name, recipient_account_no)
            print(f'R{transfer_no:.2f} successfully transferred to {recipient_name_transfer}')
    except ValueError:
        print("Please enter a valid number.")

def update_balance(amount):
    global recipient_name

    try:
        df = pd.read_csv("accounts.csv")
    except FileNotFoundError:
        print("Error: accounts.csv not found.")
        return

    mask = df['name'].str.lower() == recipient_name.lower()
    
    if mask.any():  
        index = df.index[mask].tolist()[0]
        
        df.loc[index, 'balance'] += amount       
    else:
        print(f"Account '{recipient_name}' not found in the accounts.")
        
    df.to_csv("accounts.csv", index=False)

def view_balance():
    global recipient_name

    try:
        df = pd.read_csv("accounts.csv")
    except FileNotFoundError:
        print("Error: accounts.csv not found.")
        return

    value = df['name'].str.lower() == recipient_name.lower()
    
    if value.any():  
        index = df.index[value].tolist()[0]
        
        balance = df.loc[index, 'balance']
        
        print(f"Your current balance is: R{balance:.2f}")  

    else:
        print(f"Account '{recipient_name}' not found in the accounts.")

def manage_accounts():
    options = [
        "1 - Link New Account",
        "2 - View Linked Accounts",
        "3 - View Your Account Details",
        "4 - Add New Account" 
    ]

    for option in options:
        print(option)

    choice = get_input("Please choose an option: ")

    if choice == '1':     
        # Link New Account
        account_to_link = get_input("Enter the name of the account to link: ").strip()

        df_banks = pd.read_csv("banks.csv")
        mask = df_banks['name'].str.lower() == account_to_link.lower()

        if mask.any():
            index = df_banks.index[mask].tolist()[0]
            linked_accounts = df_banks.at[index, 'linked_accounts'] if 'linked_accounts' in df_banks.columns else ""
            if pd.isna(linked_accounts):
                linked_accounts = ""
            linked_accounts_list = linked_accounts.split(",") if linked_accounts else []

            if recipient_name not in linked_accounts_list:
                linked_accounts_list.append(recipient_name)
                df_banks.at[index, 'linked_accounts'] = ",".join(linked_accounts_list)
                df_banks.to_csv("banks.csv", index=False)
                print(f"Account '{recipient_name}' successfully linked to '{account_to_link}'.")
            else:
                print(f"Account '{recipient_name}' is already linked to '{account_to_link}'.")
        else:
            print(f"Account '{account_to_link}' not found in banks. Creating a new account.")
            
            new_account_no = get_input("Enter new account number: ")
            new_account_type = get_input("Enter account type (Savings/Cheque): ")
            new_account_uid = df_banks['uid'].max() + 1 if not df_banks.empty else 0
            new_account_id = get_input("Enter your ID number: ")

            # Add the new account to banks.csv
            new_bank_account = pd.DataFrame([{
                'uid': new_account_uid, 
                'name': account_to_link, 
                'id_number': new_account_id,
                'bank_name': '',  # Update as needed
                'account_no': new_account_no,
                'linked_accounts': recipient_name
            }])
            df_banks = pd.concat([df_banks, new_bank_account], ignore_index=True)
            df_banks.to_csv("banks.csv", index=False)

            # Adding the new account to accounts.csv
            df_accounts = pd.read_csv("accounts.csv")
            new_account = pd.DataFrame([{
                'uid': new_account_uid, 
                'name': account_to_link, 
                'surname': 'unknown', 
                'account_no': new_account_no, 
                'balance': 0.0, 
                'account_type': new_account_type,
                'id_number': new_account_id,
                'linked_accounts': ""
            }])
            df_accounts = pd.concat([df_accounts, new_account], ignore_index=True)
            df_accounts.to_csv("accounts.csv", index=False)

            print(f"New account added for {account_to_link} with account number {new_account_no} - {new_account_type}.")

    elif choice == '2':
        # View Linked Accounts
        print("You selected: View Linked Accounts")
        df_banks = pd.read_csv("banks.csv")
        mask = df_banks['name'].str.lower() == recipient_name.lower()
        
        if mask.any():
            linked_accounts = df_banks.at[mask.index[0], 'linked_accounts'] if 'linked_accounts' in df_banks.columns else ""
            if pd.isna(linked_accounts):
                linked_accounts = ""
            linked_accounts_list = linked_accounts.split(",") if linked_accounts else []
            
            if linked_accounts_list:
                print(f"Linked accounts for '{recipient_name}':")
                for linked_account in linked_accounts_list:
                    print(linked_account)
            else:
                print(f"No linked accounts found for '{recipient_name}'.")
        else:
            print(f"Account '{recipient_name}' not found in banks.")

    elif choice == '3':
        # View Your Account Details
        print("Your Account Details : ")
        df_banks = pd.read_csv("banks.csv")
        mask = df_banks['name'].str.lower() == recipient_name.lower()
        
        if mask.any():
            account_details = df_banks[mask][['name', 'id_number', 'bank_name', 'account_no']]
            print(account_details.to_string(index=False))
        else:
            print(f"Account '{recipient_name}' not found in banks.")

    elif choice == '4':
        # Add New Account
        account_name = get_input("Enter the name of the new account: ").strip()
        add_new_account(account_name)

    else:
        print("Invalid option selected.")

def add_new_account(account_name):
    try:
        df_accounts = pd.read_csv("accounts.csv")
        new_account_no = get_input("Enter new account number: ")
        new_account_type = get_input("Enter account type (Savings/Cheque): ")
        new_account_uid = df_accounts['uid'].max() + 1 if not df_accounts.empty else 0
        new_account_id = get_input("Enter your ID number: ")
        
        # Adding the new account to accounts.csv
        new_account = pd.DataFrame([{
            'uid': new_account_uid, 
            'name': account_name, 
            'surname': 'unknown', 
            'account_no': new_account_no, 
            'balance': 0.0, 
            'account_type': new_account_type,
            'id_number': new_account_id,
            'linked_accounts': ""
        }])
        df_accounts = pd.concat([df_accounts, new_account], ignore_index=True)
        df_accounts.to_csv("accounts.csv", index=False)
        
        # Adding the new account to banks.csv
        df_banks = pd.read_csv("banks.csv")
        new_bank_account = pd.DataFrame([{
            'uid': new_account_uid, 
            'name': account_name, 
            'id_number': new_account_id,
            'bank_name': '',  
            'account_no': new_account_no,
            'linked_accounts': ""
        }])
        df_banks = pd.concat([df_banks, new_bank_account], ignore_index=True)
        df_banks.to_csv("banks.csv", index=False)
        
        print(f"New account added for {account_name} with account number {new_account_no} - {new_account_type}.")
    
    except FileNotFoundError:
        return


def verify_account(account_name):
    df_accounts = pd.read_csv("accounts.csv")
    mask = df_accounts['name'].str.lower() == account_name.lower()
    return mask.any()

while True: 
    print(" 1 - View Balance\n 2 - Withdraw\n 3 - Transfer\n 4 - Manage Accounts\n 5 - Exit")
    option = get_input("Please choose an option: ")

    if option == '1':
        view_balance()
    elif option == '2':
        withdraw()
    elif option == '3':
        transfer()
    elif option == '4':
        manage_accounts()
    elif option == '5':
        print("Thank you for using BankSwift")
        break
    else:
        print("Please choose a valid option")
