from datetime import datetime, timedelta
import re

class Field:
    pass

class Phone(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if re.match(r"^\+\d{10,15}$", value):
            self._value = value
        else:
            raise ValueError("Invalid phone number format")

class Birthday(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            self._value = value
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = [Phone(phone)] if phone else []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def days_to_birthday(self):
        if not self.birthday:
            return "Birthday not set"
        today = datetime.now()
        next_birthday = datetime.strptime(f"{today.year}-{self.birthday.value[5:]}", '%Y-%m-%d')
        if next_birthday < today:
            next_birthday = datetime.strptime(f"{today.year + 1}-{self.birthday.value[5:]}", '%Y-%m-%d')
        return (next_birthday - today).days

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def iterator(self, n):
        for i in range(0, len(self.records), n):
            yield self.records[i:i + n]
