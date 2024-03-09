from collections import UserDict
from functools import reduce
import datetime as dt
import pickle

class Field:
    def __init__(self, value):
        self.value = value
        self.name = value
     
    def __str__(self):
        return str(self.value) # реалізація 
  

class Name(Field): 
   
    def __init__(self):
        pass
        
             
class Phone(Field):
    MAX_LEN = 10
    def __init__(self, value):
        self.phone = value
        if len (self.phone) > 10:
            raise ValueError (f'There is too many digits in the entered phone number: {self.phone}. The max length is 10 symbols.')
    
class Birthday(Field):
   
    def __init__(self, value):
        self.birthday = value
        try:
            if dt.datetime.strptime(self.birthday, "%d.%m.%Y").date():
                return self.birthday
        except ValueError:
            raise ValueError ("Invalid date format. Use DD.MM.YYYY")  


class Record (Field):
   
    def __init__(self, name):
        self.name = Field(name)
        self.birthday = None
        self.phones= []

     
    def add_phone (self, phone):
        self.phone = Phone (phone)
        for user_phone in self.phones:
            if user_phone == phone:
                return 'Phone exists'
        self.phones.append(phone)
        return f" {self.name} : {self.phones}"

    
    def find_phone(self, phone):
        self.phone = Phone (phone)
        try:
            [self.phone for self.phone in self.phones if self.phone in self.phones]
            return f"The phone number: {self.phone} is found in {self.name} contacts"
        except: 
            raise f'The phone number: {self.phone} is not found'
  
   
    def edit_phones(self, phone, new_phone) :
        self.phone, self.new_phone = phone, new_phone
        if [self.phone for self.phone in self.phones if self.phone in self.phones]:
            self.phones = reduce(lambda a, b : a + [self.new_phone] if b == self.phone else a + [b], self.phones, [])
        return f" The contact \' {self.name} \' edited phone numbers are: {self.phones}"
            
         
    def  delete_phone (self, phone):
        self.phone = Phone (phone)
        if [self.phone for self.phone in self.phones if self.phone in self.phones]:
            self.phones.remove (self.phone)
            return f"The phone number: {self.phone} is deleted. Contact \'{self.name}\' phones remained are: {self.phones}"
        else: f" The phone number: {self.phone} is not found"

    
    def add_birthday (self, birthday:Birthday):
        self.birthday = birthday
        return f" The conract \'{self.name}\' birthday date is {self.birthday}"
    
            
    def __str__(self):
        # return f'Contact name {self.name.value}, phones: {", ".join(self.phone for self.phone in self.phones)}'
        return f" Name : \'{self.name}\' , Phone number: \'{", ".join(self.phone for self.phone in self.phones)}\', Date of birthday: \'{self.birthday}\'"
    
    def __repr__(self):
        # return f'Contact name {self.name.value}, phones: {", ".join(self.phone for self.phone in self.phones)}'
        return f" Name : \'{self.name}\' , Phone number: \'{", ".join(self.phone for self.phone in self.phones)}\', Date of birthday: \'{self.birthday}\'"
            

class AddressBook(UserDict): # реалізація класу

    def add_record (self, record): 
        name= record.name.value
        if name not in self.data:
            self.data [name] = record
            # record = Record (name)
            # record.add_phone (phone)
            # record.add_birthday (birthday)
           
            return f"Contact: {self.data [name]} - is added"
        else: 
            return f"Contact: {self.data [name]} - already exists!"
    
  
    def find_record (self, name, record):
        if name in self.data:
            return f"Contact: {name:15} : {record:15} - is found"
        else: 
            return F"Contact: {name:15} : {record:15} - is not found"
           
    def  delete_record (self, name, record):
        if name in self.data:
            self.data.pop(name) 
            return f"The contact of {name} is removed from Addressbook "
        else:
            return f'{name} is not found in the Addressbook'
        
    
    def get_upcoming_birthdays(self, birthday):
        birthday =Record(birthday)
        today_date=dt.datetime.today().date() # беремо сьогоднішню дату
        today_date.toordinal() # в дні з початку часу
        birthdays_list = [] # створюємо список для результатів
        for name in self.data: # перебираємо користувачів
            birthday=name["birthday"] # отримуємо дату народження людини у вигляді рядка
            birthday=str(today_date.year)+birthday[4:] # Замінюємо рік на поточний
            birthday=dt.datetime.strptime(birthday, "%Y.%m.%d").date() # перетворюємо дату народження в об’єкт date
            week_day= birthday.isoweekday() # Отримуємо день тижня (1-7)
            birthday_to_ord = birthday.toordinal() #в дні з початку часу
            days_between = birthday_to_ord - today_date.toordinal() # рахуємо різницю між зараз і днем народження цьогоріч у днях
            if 0<=days_between<7: # якщо день народження протягом 7 днів від сьогодні
                if week_day<6: #  якщо пн-пт
                    birthdays_list.append({'name':name['name'], 'birthday':birthday.isoformat().replace('-','.')[:10]}) 
                    # Додаємо запис у список. Isoformat дає дату у вигляді yyyy-mm-dd, тому треба замінити - на .
                else:
                    if dt.datetime.fromordinal(birthday_to_ord+1).weekday()==0:# якщо неділя
                        birthdays_list.append({'name':name['name'], 'birthday':dt.datetime.fromordinal(birthday_to_ord+1).isoformat().replace('-','.')[:10]})
                        #Переносимо на понеділок. Додаємо запис у список. Isoformat дає дату у вигляді yyyy-mm-dd, тому треба замінити - на .
                    elif dt.datetime.fromordinal(birthday_to_ord+2).weekday()==0: #якщо субота
                        birthdays_list.append({'name':name['name'], 'birthday':dt.datetime.fromordinal(birthday_to_ord+2).isoformat().replace('-','.')[:10]})
                        #Переносимо на понеділок. Додаємо запис у список. Isoformat дає дату у вигляді yyyy-mm-dd, тому треба замінити - на .
            return birthdays_list  #return {"name":name, "congratulation_date":cdate}

    
    def save_data (book, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(book, f)

    def load_data(filename="addressbook.pkl"):

        try:
            with open(filename, "rb", ) as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

 # Бот для завантаження і перевірки даних:        

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Not found"
        except Exception as e:
            return f"Error: {e}"
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone, birthday, *_ = args
    record = book.get(name)
    message = "Contact is updated." 
    if record is None:
        record = Record(name)
        AddressBook.add_record (args)
        message = "Contact is added."
    if phone:
        record.add_phone(phone)
        return message
    if birthday:
        record.add_birthday (args)
        return message
    else:
        raise(KeyError)
    

@input_error
def remove_contact(args, book):
    name, *_= args 
    message = "Contact is deleted."
    record = Record(name)
    if record in book:
        record = Record(name)
        AddressBook.delete_record (name)
        return message 
    else:
        raise(KeyError)
    
    
@input_error
def show_contact (args, book):
    name, *_ = args
    message = "Contact is found"
    record = Record(name)
    if record in book:
        AddressBook.find_record(name)
        return message
    else:
        raise(KeyError)
     

@input_error
def add_phone(args, book):
    name, phone,*_ = args
    record = Record(name)
    if phone is None:
        return record.add_phone(args)
    else: 
        raise (KeyError)
    
@input_error
def show_phone(args,book):
    name, phone,*_ = args
    record = Record(name)
    if record:
        return record.find_phone(args)
    else: 
        raise(KeyError)
    
     
@input_error
def change_phone(args,book):
    name, phone, new_phone,*_ = args
    record = Record(name)
    if record:
        return record.edit_phones(args)
    else: 
        raise(KeyError)
    
@input_error
def remove_phone(args,book): 
    name, phone, *_ = args
    record = Record(name)
    if record:
        return record.delete_phone(args)
    else: 
        raise(KeyError)
    
@input_error
def show_birthday (args, book):
    name, birthday, *_ = args
    record = Record(name)
    if record in book:
        return record.add_birthday (args)
    else: 
        raise(KeyError)
    
@input_error
def add_bdate (args, book):
    name, birthday, *_ = args 
    record = Record(name)
    if record in book:
        return add_contact (args)
    else:
        raise(KeyError)
    
@input_error
def show_all(args, book):
    name, *_= args
    s=''
    for name in book:
        s+=(f"{name:15} : {book[name]}\n")
    return s


def main():
    book = AddressBook()
    book =AddressBook.load_data()

    # For testing
    # ===============================================================
    print("Welcome to the assistant bot!")
    print('\nAdding Edd...\n')
    print(add_contact(['Edd', '1234567890', '16.06.1996'], book))

    print('\nShowing all...\n')
    print(show_all([], book))

    print('\nAdding phone...\n')
    print(add_phone(['Edd', '0987654321'], book))

    print('\nChanging phone...\n')
    print(change_phone(['Edd', '1234567890', '1234567899'], book))
    # ===============================================================
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input (user_input)

        if command in ["close", "exit"]:
            AddressBook.save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")
        
        elif command == "add_phone":
            print(add_phone (args, book))
        
        elif command == "change_phone":
            print(change_phone (args, book))

        elif command == "delete_phone":
            print(remove_phone (args, book))
        
        elif command == "show_phone":
            print(show_phone(args,book))

        elif command == "add_contact":
            print(add_contact (args, book))

        elif command == "change_contact":
            print (change_contact(args, book))
        
        elif command == "show_all":
            print(show_all (args,book))

        elif command == "add_birthday":
            print(add_bdate (args,book))

        elif command == "show_birthday":
            print(show_birthday (args,book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()          
