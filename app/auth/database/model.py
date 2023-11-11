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
    type = Column(String(50), nullable=False, index=True)
    email = Column(EmailType, nullable=False, unique=True, index=True)
    company = Column(String)
    position = Column(String)


# class Token(Base):
#     __tablename__ = "token"

#     token = Column(UUIDType, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
    
#     user = relationship("User", lazy="joined")

# class Token(Base):
#     __tablename__ = "token"

#     token = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     access_token: type = Column(String, nullable=False)
#     token_type: type = Column(String, nullable=False)
    
#     user = relationship("User", lazy="joined")


class Password(Base):
    __tablename__ = "password"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True)
    password = Column(String, nullable=False)

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



ORM_MODEL_CLS = Type[User] | Type[Password] | Type[Phone] \
                | Type[Adress] | Type[Contact]

ORM_MODEL = User | Password | Phone \
                | Adress | Contact