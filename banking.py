import datetime
import csv
import pandas as pd

balance = float()
account_type = "Savings Acc"
account_name = "User"
recipient_name = input("Enter recipient account name: ")


def write_transaction(transaction_type, amount, account_type, account_name, to_account=None):
    transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if to_account:
        from_account_name = get_account_name(account_name)
        to_account_name = get_account_name(to_account)
        transaction_details = f"{transaction_time} - {transaction_type}: R{amount:.2f} - From: {from_account_name} ({account_type}) - To: {to_account_name}\n" #withdraw & deposit
    else:
        from_account_name = get_account_name(account_name)
        transaction_details = f"{transaction_time} - {transaction_type}: R{amount:.2f} - From: {from_account_name} ({account_type})\n" #transfers

    with open("transactionslog.txt", "a") as file:
        file.write(transaction_details)

def get_input(prompt):
    return input(prompt).strip()

def get_account_name(account_number):
    with open("accounts.txt", "r") as file:
        lines = file.readlines()[1:]  
        for line in lines:
            parts = line.strip().split(',')
            if parts[3] == account_number:
                return parts[1]
    return "User"

def deposit():
    global balance
    try:
        deposit_no = float(get_input("Enter amount to deposit: "))
        if deposit_no <= 0:
            print("Amount must be greater than zero.")
        else:
            balance += deposit_no
            print(f'R{deposit_no:.2f} successfully deposited into account.')
            write_transaction("Deposit", deposit_no, account_type, account_name)
    except ValueError:
        print("Please enter a valid number.")

def withdraw():
    global balance
    try:
        withdraw_no = float(get_input("Enter amount to withdraw: "))
        if withdraw_no <= 0:
            print("Amount must be greater than zero.")
        elif withdraw_no > balance:
            print("Insufficient funds.")
        else:
            balance -= withdraw_no
            print(f'R{withdraw_no:.2f} successfully withdrawn.')
            write_transaction("Withdraw", withdraw_no, account_type, account_name)
    except ValueError:
        print("Please enter a valid number.")

def show_available_accounts():
    print("Available accounts:")
    with open("accounts.txt", "r") as file:
        lines = file.readlines()[1:]
        for line in lines:
            parts = line.strip().split(',')
            print(f"Recipient: {parts[1]}, Account_no: {parts[3]}")

def transfer():
    global balance
    show_available_accounts()

    try:
        recipient_name = get_input("Enter recipient account name: ")

        # Check if account exists
        account_exists = False
        with open("accounts.txt", "r") as file:
            lines = file.readlines()[1:] 
            for line in lines:
                parts = line.strip().split(',')
                if parts[1].lower() == recipient_name.lower():
                    account_exists = True
                    recipient_account_no = parts[3]
                    break

        if not account_exists:
            create_new = get_input("Account not found. Do you want to create a new account? (yes/no): ").lower()
            if create_new == 'yes':
                recipient_account_no = get_input("Enter new account number for recipient: ")
                new_account_uid = len(lines) 

                #writes into file
                with open("accounts.txt", "a") as file:
                    file.write(f"{new_account_uid},{recipient_name},unknown,{recipient_account_no}\n")
                print(f'New account created for {recipient_name} with account number {recipient_account_no}')
            else:
                print("Transfer cancelled.")
                return

        transfer_no = float(get_input("Enter amount to transfer: "))
        if transfer_no <= 0:
            print("Amount must be greater than zero.")
        elif transfer_no > balance:
            print("Insufficient funds.")
        else:
            balance -= transfer_no
            write_transaction("Transfer", transfer_no, account_type, account_name, recipient_account_no)
            print(f'R{transfer_no:.2f} successfully transferred to {recipient_name}')
    except ValueError:
        print("Please enter a valid number.")

def view_balance():
    global balance
    print(f"Your current balance is: R{balance:.2f}")

def update_balance():
    global balance
    global recipient_name

    with open("accounts.csv", "r") as file:
        specific_balance = float()
        
        for line in file:
            if recipient_name in line:
                Current_line = line
                selected_line = Current_line.split(",")
                if len(selected_line) >= 3 :
                    specific_balance = float(selected_line[4])

                balance = specific_balance + balance                  
                return balance
    

while True:
    x= update_balance()
    print(x, "balance")


    print(" 1 - Deposit\n 2 - Withdraw\n 3 - View Balance\n 4 - Transfer\n 5 - Exit")
    option = get_input("Please choose an option: ")

    if option == '1':
        deposit()
    elif option == '2':
        withdraw()
    elif option == '3':
        view_balance()
    elif option == '4':
        transfer()
    elif option == '5':
        print("Thank you for using BankSwift")
        break
    else:
        print("Please choose a valid option")
