from typing import Type

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType, ChoiceType, PhoneNumber, UUIDType


from .database import Base


class User(Base):
    __tablename__ = "user"

    USER_TYPE_CHOICES = [
        ('shop', 'Магазин'),
        ('buyer', 'Покупатель')
    ]

    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    surename = Column(String(50))
    type = Column(ChoiceType(USER_TYPE_CHOICES), nullable=False, index=True)
    email = Column(EmailType, nullable=False, unique=True, index=True)
    company = Column(String)
    position = Column(String)


class Token(Base):
    __tablename__ = "token"

    token = Column(UUIDType, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", lazy="joined")


class Password(Base):
    __tablename__ = "password"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    password = Column(String(60), nullable=False)

    user = relationship("User", lazy="joined")


class Phone(Base):
    __tablename__ = "phone"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(13), nullable=False, unique=True)


class Adress(Base):
    __tablename__ = "adress"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    street = Column(String(50), nullable=False)
    house = Column(String(50), nullable=False)
    office = Column(String(50))


class Contact(Base):
    __tablename__ = "contact"

    CONTACT_TYPE_CHOICES = [
        ('phone', 'Телефон'),
        ('adress', 'Адресс')
    ]

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    type = Column(ChoiceType(CONTACT_TYPE_CHOICES), nullable=False, index=True)
    phone_id = Column(Integer, ForeignKey("phone.id", ondelete="CASCADE"))
    adress_id = Column(Integer, ForeignKey("adress.id", ondelete="CASCADE"))

    user = relationship("User", lazy="joined")
    phone = relationship("Phone", lazy="joined")
    adress = relationship("Adress", lazy="joined")


class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False)
    url = Column(String, unique=True)
    filename = Column(String, unique=True)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)


class Shop_category(Base):
    __tablename__ = "shop_category"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shop.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
    
    shop = relationship("Shop", lazy="joined")
    category = relationship("Category", lazy="joined")


class ProductInfo(Base):
    __tablename__ = "productInfo"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shop.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    quntity = Column(Integer, nullable=False)
    price = Column(Numeric(15,2), nullable=False)
    price_rcc = Column(Numeric(15,2), nullable=False)
    model = Column(String(50))
    paramentrs = Column(JSON)

    shop = relationship("Shop", lazy="joined")
    category = relationship("Category", lazy="joined")


class Shopping(Base):
    __tablename__ = "shopping"

    id = Column(Integer, primary_key=True, index=True)
    productInfo_id = Column(Integer, ForeignKey("productInfo.id", ondelete="CASCADE"), nullable=False)
    quntity = Column(Integer, nullable=False)
    shoppingCart_id = Column(Integer, ForeignKey("shoppingCart.id", ondelete="CASCADE"))

    productInfo = relationship("ProductInfo", lazy="joined")
    shopping = relationship("ShoppingCart", lazy="joined")
    

class ShoppingCart(Base):
    __tablename__ = "shoppingCart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    # shopping_id = Column(Integer, ForeignKey("shopping.id", ondelete="CASCADE"))

    user = relationship("User", lazy="joined")
    # shopping = relationship("Shopping", lazy="joined")


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contact.id", ondelete="CASCADE"))
    shoppingCart_id = Column(Integer, ForeignKey("shoppingCart.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())

    contact = relationship("Contact", lazy="joined")
    shoppingCart = relationship("ShoppingCart", lazy="joined")


ORM_MODEL_CLS = Type[User] | Type[Token] | Type[Password] | Type[Phone] \
                | Type[Adress] | Type[Contact] | Type[Shop] | Type[Category] \
                | Type[Shop_category] | Type[ProductInfo] | Type[Shopping] \
                | Type[ShoppingCart] | Type[Order]

ORM_MODEL = User | Token | Password | Phone \
                | Adress | Contact | Shop | Category \
                | Shop_category | ProductInfo | Shopping \
                | ShoppingCart | Order