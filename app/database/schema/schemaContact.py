from typing import Optional

from pydantic import BaseModel

from schema.schemaUser import User


class PhoneBase(BaseModel):
    phone: str


class PhoneCreate(PhoneBase):
    pass


class PhonePatch(BaseModel):
    phone: str


class Phone(PhoneBase):
    id: int

    class Congig:
        orm_mode = True


class AdressBase(BaseModel):
    region: str
    city: str
    street: str
    house: str
    office: str


class AdressCreate(AdressBase):
    pass


class AdressPatch(BaseModel):
    region: Optional[str]
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]
    office: Optional[str]


class Adress(AdressBase):
    id: int

    class Congig:
        orm_mode = True


class ContactBase(BaseModel):
    user_id: int
    type: str
    phone: list[Phone]
    adress_id: list[Adress]

class ContactCreate(ContactBase):
    pass


class ContactPatch(BaseModel):
    pass


class Contact(ContactBase):
    id: int
    user: User
    phone: list[Phone]
    adress_id: list[Adress]

    class Congig:
        orm_mode = True