from collections import UserDict
import re  # Для валідації номерів телефонів

## Базовий клас для всіх полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

## Клас для зберігання імені контакту (обов'язкове поле)
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")  # Перевірка на порожнє ім'я
        super().__init__(value)

## Клас для зберігання номеру телефону з валідацією (10 цифр)
class Phone(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid phone number. Must be 10 digits.")
        super().__init__(value)

    # Валідація формату телефону (10 цифр)
    @staticmethod
    def is_valid(phone):
        return bool(re.match(r"^\d{10}$", phone))

## Клас для зберігання інформації про контакт (ім'я + телефони)
class Record:
    def __init__(self, name):
        self.name = Name(name)  # Ім'я контакту обов'язково
        self.phones = []

    # Додавання телефону до контакту
    def add_phone(self, phone):
        self.phones.append(Phone(phone))  # Додаємо телефон у вигляді об'єкта Phone

    # Видалення телефону з контакту
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break                                 # break — після того як ми знайшли потрібний телефон і видалили його, немає потреби далі перевіряти інші телефони в списку. Тому команда break зупиняє виконання циклу.
                                                      # Навіщо використовується break? Продуктивність: Якщо ми знайшли телефон, який потрібно видалити, немає сенсу далі продовжувати перевіряти інші телефони у списку. Команда break зупиняє цикл, що дозволяє заощадити ресурси і час виконання програми. Логіка: Після видалення телефону достатньо лише одного проходу через список, тому break допомагає уникнути зайвих операцій.
    # Редагування телефону в контакті
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    # Пошук телефону в контакті
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


## Клас для зберігання та управління адресною книгою (словник)
class AddressBook(UserDict):
    # Додавання запису в книгу контактів
    def add_record(self, record):
        self.data[record.name.value] = record         # self.data — це атрибут, успадкований від UserDict, і він містить внутрішнє сховище даних. Це фактично звичайний словник, в якому ключами будуть імена контактів, а значеннями — самі об'єкти Record.
                                                      # record.name.value — тут ми звертаємося до атрибута name об'єкта record, який є об'єктом класу Name. У класі Name ми зберігаємо значення імені, і звернення до record.name.value дає доступ до самого імені контакту.
                                                      # record — це сам об'єкт Record, який ми додаємо до адресної книги. Він містить всю інформацію про контакт, зокрема ім'я та телефони.

    # Пошук запису за іменем
    def find(self, name):
        return self.data.get(name)

    # Видалення запису з книги за іменем
    def delete(self, name):
        if name in self.data:
            del self.data[name]




### Тестування функціональності

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
print("All contacts:")
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
if john:
    john.edit_phone("1234567890", "1112223333")

print("\nAfter editing John's phone:")
print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"\nFound phone for John: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

# Виведення всіх записів у книзі після видалення Jane
print("\nAll contacts after deleting Jane:")
for name, record in book.data.items():
    print(record)


    

