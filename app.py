from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import get_db, engine
from models.user import User
from models.item import Item
from schemas.user import User, UserCreate
from schemas.item import Item, ItemCreate
from sqlalchemy.exc import IntegrityError

# Ініціалізація FastAPI
app = FastAPI()

# Створення таблиць в базі даних
User.metadata.create_all(bind=engine)
Item.metadata.create_all(bind=engine)

# Реєстрація нового користувача
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, password_hash=user.password)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this username or email already exists")
    return db_user

# Створення нового товару
@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
