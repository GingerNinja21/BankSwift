balance = 0

def deposit():
    global balance
    
    try:
        deposit_no = float(input("Enter amount to deposit: ")) 
        if deposit_no <= 0:
            print("Amount must be greater than zero.")
        else:
            balance += deposit_no 
            print("Your current balance is: R" + str(balance))
    except ValueError:
        print("Please enter a valid number.")

def withdraw():
    global balance
    
    try:
        withdraw_no = float(input("Enter amount to withdraw: "))
        if withdraw_no <= 0:
            print("Amount must be greater than zero.")
        elif withdraw_no > balance:
            print("Insufficient funds.")
        else:
            balance -= withdraw_no 
            print("Your current balance is: R" + str(balance))
    except ValueError:
        print("Please enter a valid number.")


while True:
    print(" 1 - Deposit\n 2 - Withdraw\n 3 - Cancel")
    option = input("Please choose an option: ").strip()

    if option == '1':
        deposit()
    elif option == '2':
        withdraw()
    elif option == '3':
        print("Thank you for using BankSwift")
        break
    else:
        print("Invalid Choice")
