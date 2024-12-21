import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import time
from sqlalchemy.orm import Session
from models.user import User
from models.item import Item
from db import engine, get_db

# Функція для вимірювання часу виконання запиту
def measure_time(func):
    start_time = time.time()
    func()
    end_time = time.time()
    return end_time - start_time

# Тестування SELECT запиту
def select_test(db: Session, n: int):
    users = db.query(User).limit(n).all()
    items = db.query(Item).limit(n).all()

# Тестування INSERT запиту
def insert_test(db: Session, n: int):
    for _ in range(n):
        db_user = User(username="user", email="user@example.com", password_hash="password")
        db_item = Item(name="item", description="item description", price=100)
        db.add(db_user)
        db.add(db_item)
    db.commit()

# Тестування UPDATE запиту
def update_test(db: Session, n: int):
    users = db.query(User).limit(n).all()
    for user in users:
        user.username = "updated_username"
    db.commit()

# Тестування DELETE запиту
def delete_test(db: Session, n: int):
    users = db.query(User).limit(n).all()
    for user in users:
        db.delete(user)
    db.commit()

# Тестування запитів для різної кількості даних
def perform_tests():
    for n in [1000, 10000, 100000, 1000000]:
        print(f"Testing with {n} records:")
        with next(get_db()) as db:
            print(f"  SELECT: {measure_time(lambda: select_test(db, n))} seconds")
            print(f"  INSERT: {measure_time(lambda: insert_test(db, n))} seconds")
            print(f"  UPDATE: {measure_time(lambda: update_test(db, n))} seconds")
            print(f"  DELETE: {measure_time(lambda: delete_test(db, n))} seconds")

# Виконання тестів
if __name__ == "__main__":
    perform_tests()
