from datetime import datetime, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Invalid phone number format.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = datetime.today()
        next_week_start = today + timedelta(days=(6 - today.weekday()) + 7)
        next_week_end = next_week_start + timedelta(days=6)

        upcoming_birthdays = []
        for name, record in self.data.items():
            if record.birthday:
                birth_date = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                if next_week_start <= birth_date <= next_week_end:
                    upcoming_birthdays.append(f"{name}: {record.birthday}")

        return upcoming_birthdays


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"

    return inner


@input_error
def add_contact(args, book):
    if len(args) == 2:
        name, phone = args
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return f"Contact added: {record}"
    else:
        raise ValueError("Invalid command. Please provide both name and phone.")


@input_error
def change_contact(args, book):
    if len(args) == 2:
        name, phone = args
        record = book.find(name)
        if record:
            record.edit_phone(record.phones[0].value, phone)
            return f"Contact updated: {record}"
        else:
            raise ValueError(f"Contact with name '{name}' not found.")
    else:
        raise ValueError("Invalid command. Please provide both name and phone.")


@input_error
def show_phone(args, book):
    if len(args) == 1:
        name = args[0]
        record = book.find(name)
        if record:
            return f"Phone for {name}: {record.phones[0]}"
        else:
            raise ValueError(f"Contact with name '{name}' not found.")
    else:
        raise ValueError("Invalid command. Please provide the name.")


@input_error
def show_all(book):
    if book:
        for name, record in book.items():
            print(record)
    else:
        return "No contacts available."


@input_error
def add_birthday(args, book):
    if len(args) == 2:
        name, birthday = args
        record = book.find(name)
        if record:
            record.add_birthday(birthday)
            return f"Birthday added for {name}: {record.birthday}"
        else:
            raise ValueError(f"Contact with name '{name}' not found.")
    else:
        raise ValueError("Invalid command. Please provide both name and birthday.")


@input_error
def show_birthday(args, book):
    if len(args) == 1:
        name = args[0]
        record = book.find(name)
        if record:
            return f"Birthday for {name}: {record.birthday}"
        else:
            raise ValueError(f"Contact with name '{name}' not found.")
    else:
        raise ValueError("Invalid command. Please provide the name.")


@input_error
def birthdays(book):
    upcoming_birthdays = book.get_birthdays_per_week()
    if upcoming_birthdays:
        return "Upcoming birthdays:\n" + "\n".join(upcoming_birthdays)
    else:
        return "No upcoming birthdays in the next week."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        try:
            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                show_all(book)
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(book))
            else:
                print("Invalid command.")
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
