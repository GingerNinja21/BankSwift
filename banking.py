import datetime

balance = 0

def write_transaction(transaction_type, amount):
    transaction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction_details = f"{transaction_time} - {transaction_type}: R{amount:.2f}\n"
    
    with open("transactionslog.txt", "a") as file:
        file.write(transaction_details)

def get_input(prompt):
    return input(prompt).strip()

def deposit():
    global balance
    try:
        deposit_no = float(get_input("Enter amount to deposit: "))
        if deposit_no <= 0:
            print("Amount must be greater than zero.")
        else:
            balance += deposit_no
            write_transaction("Deposit", deposit_no)
            return deposit_no 
        
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
            write_transaction("Withdraw", withdraw_no)
            return withdraw_no 
        
    except ValueError:
        print("Please enter a valid number.")

def view_balance():
    global balance
    print(f"Your current balance is: R{balance:.2f}")
    return balance  

while True:
    print(" 1 - Deposit\n 2 - Withdraw\n 3 - View Balance\n 4 - Cancel")
    option = get_input("Please choose an option: ")

    if option == '1':
        deposited_amount = deposit()
    elif option == '2':
        withdrawn_amount = withdraw()
    elif option == '3':
        view_balance()
    elif option == '4':
        print("Thank you for using BankSwift")
        break
    else:
        print("Please choose a valid option")