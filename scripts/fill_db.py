import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from models.user import User
from models.item import Item
from db import engine, get_db
import random
import string

# Функція для генерації випадкових рядків
def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Скрипт для додавання користувачів та товарів в БД
def fill_db(db: Session, n: int):
    for _ in range(n):
        username = random_string()
        email = f"{username}@example.com"
        password_hash = random_string(12)
        db_user = User(username=username, email=email, password_hash=password_hash)
        db.add(db_user)

        item_name = random_string(5)
        description = random_string(20)
        price = random.randint(1, 1000)
        db_item = Item(name=item_name, description=description, price=price)
        db.add(db_item)

    db.commit()
    db.close()

# Виконання скрипта
if __name__ == "__main__":
    with next(get_db()) as db:
        fill_db(db, 1000)  # Наповнення БД 1000 записами
