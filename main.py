import json
import random
from pathlib import Path
import string


class Bank:
    database = "data.json"
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
          print("Database not found. A new one will be created after first account creation.")


    except Exception as e:
        print("An error occurred:", e)

    @classmethod
    def __update(cls):
        with open (cls.database, 'w') as fs:
         fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountnumbergenerate(cls):
        alpha = random.choices(string.ascii_letters , k=5)
        num = random.choices(string.digits, k=5)
        ac_num = alpha + num 
        random.shuffle(ac_num)
        return "".join(ac_num)


    def create_account(self):
        info = {
            "Name" : input("Enter your name:"),
            "Age" : int(input("Enter your age:")),
            "Address": input("Enter your address:"),
            "Mobile Number": int(input("Enter your mobile number:")),
            "Father's / Husband's Name": input("Enter your Father's / Husband's Name:"),
            "Pin" : int(input("Set your 4 digit pin:")),
            "Account Number": Bank.__accountnumbergenerate(),
            "Balance": 0
        }
        if info["Age"]<18 or len(str(info["Pin"])) !=4 or len(str(info["Mobile Number"])) !=10:
            print("Invalid details provided. Account creation failed.")
        else:
            print("Account created successfully.")
            for i in info:
                print(f"{i}: {info[i]}")
            print("Please keep your account number safe for future reference.")
            Bank.data.append(info)
            Bank.__update()

    def depositmoney(self):
        account_num = input("Enter your account number:")
        pin = int(input("Enter your pin:"))

        userdata = [i for i in Bank.data if i['Account Number']== account_num and i['Pin']== pin]

        if userdata == False:
            print("No account found with the provided details.")
        else:
            amount = int(input("Enter the amount to be deposited:"))
            if amount<0 and amount>10000:
                print("Amount should be between 0 and 10,000.")
            else:
                userdata[0]['Balance'] += amount
                
                Bank.__update()
                print(f"Amount {amount} deposited successfully")
    
    def withdrawmoney(self):
        account_num = input("Enter your account number:")
        pin = int(input("Enter your pin:"))

        userdata = [i for i in Bank.data if i['Account Number']== account_num and i['Pin']== pin]
        if userdata ==False:
            print("No account found with the provided details.")
        else:
            amount = int(input("Enter the amount to be withdrawn:"))
            if amount<0 and amount>10000:
                print("Amount should be between 0 and 10,000.")
            elif userdata[0]['Balance'] < amount:
                print("Insufficient balance.")
            else:
                userdata[0]['Balance'] -= amount
                Bank.__update()
                print(f"Amount {amount} withdrawn successfully")
                print(f"Available balance is {userdata[0]['Balance']}")

    def viewdetails(self):
        account_num = input("Enter your account number:")
        pin = int(input("Enter your pin:"))

        userdata = [i for i in Bank.data if i['Account Number']== account_num and i['Pin']== pin]
        if userdata ==False:
            print("No account found with the provided details.")
        else: 
            print("Account details are as follows:")
            for i in userdata[0]:
                print(f"{i}: {userdata[0][i]}")

    def updatedetails(self):
         account_num = input("Enter your account number:")
         pin = int(input("Enter your pin:"))

         userdata = [i for i in Bank.data if i['Account Number']== account_num and i['Pin']== pin]
         if userdata ==False:
            print("No account found with the provided details.")
         else:
             print("Press 1 to update Name")
             print("Press 2 to update Address")
             print("Press 3 to update Mobile Number")
             print("Press 4 to change Father's / Husband's Name")
             choose = int(input("Enter your choice:"))
             if choose == 1:
                 name = input("Enter your new name:")
                 userdata[0]['Name'] = name
             elif choose == 2:
                 address = input("Enter your new address:")
                 userdata[0]['Address'] = address
             elif choose ==3:
                 mobile = int(input("Enter your new mobile number:"))
                 if len(str(mobile)) !=10:
                     print("Invalid mobile number.")
                 else:
                     userdata[0]['Mobile Number'] = mobile
             elif choose ==4:
                     fname = input("Enter your new Father's / Husband's Name:")
                     userdata[0]["Father's / Husband's Name"] = fname
             else:
                     print("Invalid choice.")
                     
                     
         Bank.__update()
         print("Details updated successfully.")

    def deleteaccount(self):
        account_num = input("Enter your account number:")
        pin = int(input("Enter your pin:"))

        userdata = [i for i in Bank.data if i['Account Number']== account_num and i['Pin']== pin]
        if userdata ==False:
            print("No account found with the provided details.")
        else:
            check = input("Press Y to delete account and N to not :")
            if check == 'N' or check == 'n':
                print("Account deletion cancelled.")
            else:
             index = Bank.data.index(userdata[0])
             Bank.data.pop(index)
             print("Account deleted successfully.")
            Bank.__update()


user = Bank()
print("Press 1 for creating an account")
print("Press 2 for depositing the money")
print("Press 3 for withraw the money")
print("Press 4 for viewing the account details")
print("Press 5 for updating the details")
print("Press 6 for deleting the account")

choice = int(input("Enter your choice:"))
if choice == 1:
    user.create_account()
elif choice == 2:
    user.depositmoney()
elif choice==3:
    user.withdrawmoney()
elif choice==4:
    user.viewdetails()
elif choice==5:
    user.updatedetails()
elif choice==6:
    user.deleteaccount()
else:
    print("Invalid choice")