import requests
import json
import pprint

url = 'http://127.0.0.1:8080/api/contacts/'

# Define the class for datastructure
class Contact:

    def __init__(self, phone, sex, name) -> None:
        self.setPhone(phone)
        self.setSex(sex)
        self.name = name

# check the format of user input for a phone number     
    def setPhone(self, phone) -> None:
            if not phone.isdigit():
                raise ValueError("Invalid format")
            self.phone = phone.strip()
                
# check the format of user input for sex      
    def setSex(self, sex) -> None: 
        upper = sex.upper()
        if upper in ['F','FEMALE']:
            self.sex = 'Female'
        elif upper in ['M','MALE']:
            self.sex = 'Male'
        else: 
            raise ValueError("Invalid sex format")

    def print(self):
        print(self.phone + " " + self.sex + " " + self.name)
        

def contactBook():
    while True:
        print("Please select your operation. List(L) / Read(R) / Add(A) / Edit(E) / Delete(D) / Quit(Q): \n")
        op = str.upper(input())

        match op:
            case 'A':
                print("Please input phone number,sex and name, separated by colon(;): \n ")

                 # Format the input 
                txt = input().strip()
                parts = txt.split(";")

                if len(parts) >= 3:
                    add_Data(*parts[:3])
                else:
                    print("Invalid format.")
                    return
                
            case 'R':
                print("Please input the phone number to view: \n ")

                check_phone = input()
                validate_input(check_phone)   
                read_Data(check_phone)

            case 'L':
                list_Data()
            
            case 'D':
                print("Please input the phone number to delete")

                check_phone = input()
                validate_input(check_phone)    
                delete_Data(check_phone)
            
            case 'E':
                print("Please input the phone number to update")

                check_phone = input()
                validate_input(check_phone)
                edit_Data(check_phone)
            
            case 'Q':
                print("Goodbye.")
                break
        
            case _:
                print("Invalid operation.")

# Add a contact item post request
def add_Data(new_phone, new_sex, new_name) -> None: 
    try:
        c = Contact(new_phone, new_sex, new_name)
    except ValueError as e:
        print(e)
        return

    contactItem ={
        'Phone': c.phone,
        'Sex': c.sex,
        'Name': c.name,
        }
    
    # request_string = json.dumps(contactItem)
    #request_json = json.loads(request_string)

    response = requests.post(url, json = contactItem)
    if response.status_code == 201:
        response_json = response.json()
        count = response_json['count']
        print("New contact added. Total count is {}.".format(count))
    elif response.status_code == 409:
        print("Phone number already exists.")
        return
    
    

# Read a contact item from the contact List
def read_Data(check_phone, silientMode = False) -> Contact:
    new_url = url + check_phone
    response = requests.get(new_url)
    if response.status_code == 200:
        obj = response.json()
        contact = Contact(
            obj['Phone'],
            obj['Sex'],
            obj['Name'],
        )
        if silientMode == False:
            contact.print()
        return contact
    else:
        if silientMode == False:
            print("Contact not found")
        return None
            

# List all the data from the contact list
def list_Data():
    response = requests.get(url)
    if response.status_code == 200:
        objs = response.json()
        #contact_list = []

        for obj in objs:
            contact = Contact(
                obj['Phone'],
                obj['Sex'],
                obj['Name'],
            )
            contact.print()
    else:
        print("Unknown error.{}".format(response.status_code))
        return 


# Delete data from the contact list
def delete_Data(check_phone):
    new_url = url + check_phone
    response = requests.delete(new_url)
    if response.status_code == 204:
        count = response.json()['count']
        print("Contact deleted. Total count is {}.".format(count))
    else:
        print("Contact not found")
        return


# Edit data from the contact list
def edit_Data(check_phone):

    contact = read_Data(check_phone, True)
    if contact != None:
        print("Update sex: \n ")
        update_sex = input()
        print("Update name: \n ")
        update_name = input()

        try:
            x = Contact(check_phone, update_sex, update_name)
        except ValueError as e:
            print(e)
            return

        newItem ={
            "Phone": check_phone,
            "Sex": x.sex,
            "Name": x.name,
            }
        new_url = url + check_phone
        response = requests.put(new_url, json = newItem)
        if response.status_code == 200:
            print("Contact updated.")
        else:
            print("Failed to unpdate")
            return
    else: 
        print("Contact not found")
        return



# Verify if the input phone is validate
def validate_input(check_phone):
    try:
        intphone = int(check_phone)
    except ValueError:
        print("Invalid format.")
        return

contactBook()