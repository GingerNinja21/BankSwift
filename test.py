import datetime
import pandas as pd

balance = 0.0
account_name = ""
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
    return None

def get_account_type(account_name):
    df = pd.read_csv("accounts.csv")
    account = df[df['name'].str.lower() == account_name.lower()]
    if not account.empty:
        account_type = account['account_type'].values[0]
        print(f"Using saved account type: {account_type}")
        return account_type
    else:
        print(f"Account '{account_name}' not found.")
        print("Creating new account.")
        new_account_no = get_input("Enter new account number: ")
        new_account_type = get_input("Enter account type (Savings/Cheque): ")
        new_account_uid = df['uid'].max() + 1 if not df.empty else 0
        new_account = pd.DataFrame([{
            'uid': new_account_uid, 
            'name': account_name, 
            'surname': 'unknown', 
            'account_no': new_account_no, 
            'balance': 0.0, 
            'account_type': new_account_type
        }])
        df = pd.concat([df, new_account], ignore_index=True)
        df.to_csv("accounts.csv", index=False)
        print(f"New account created for {account_name} with account number {new_account_no} and account type {new_account_type}.")
        return new_account_type

account_type = get_account_type(recipient_name)

def withdraw():
    global balance
    try:
        withdraw_no = float(get_input("Enter amount to withdraw: "))
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
    global balance
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

                new_account = pd.DataFrame([{
                    'uid': new_account_uid, 
                    'name': recipient_name_transfer, 
                    'surname': 'unknown', 
                    'account_no': recipient_account_no, 
                    'balance': 0.0, 
                    'account_type': 'Cheque'
                }])
                df = pd.concat([df, new_account], ignore_index=True)
                df.to_csv("accounts.csv", index=False)
                print(f'New account created for {recipient_name_transfer} with account number {recipient_account_no}')
            else:
                print("Transfer cancelled.")
                return
        else:
            recipient_account_no = account['account_no'].values[0]

        transfer_no = float(get_input("Enter amount to transfer: "))
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
    global balance
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
        balance = df.loc[index, 'balance']      
        print(f"Your current balance is: R{balance:.2f}")
    else:
        print(f"Account '{recipient_name}' not found in the accounts.")
        
    df.to_csv("accounts.csv", index=False)

def view_balance():
    global balance
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

while True:
    print(" 1 - Withdraw\n 2 - View Balance\n 3 - Transfer\n 4 - Exit")
    option = get_input("Please choose an option: ")

    if option == '1':
        withdraw()
    elif option == '2':
        view_balance()
    elif option == '3':
        transfer()
    elif option == '4':
        print("Thank you for using BankSwift")
        break
    else:
        print("Please choose a valid option")
