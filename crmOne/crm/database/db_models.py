from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, String, MetaData,
    DateTime, Text, ForeignKey,
    Float
)

Base = declarative_base(metadata=MetaData())


class Setting(Base):
    __tablename__ = 'settings'

    id = Column(String, primary_key=True)
    app_config = Column(Text)


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    meta_data = Column(Text)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False)
    meta_data = Column(Text)

    contact_ids = Column(String, ForeignKey('contacts.id'))


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(String, primary_key=True)
    name = Column(String(50), nullable=False)
    contact_info = Column(Text)

    status = Column(String, default="Lead", nullable=False)

    company_id = Column(String, ForeignKey('companies.id'))
    interactions = Column(String, ForeignKey('interactions.id'))

    meta_data = Column(Text, nullable=False)


class Interaction(Base):
    __tablename__ = 'interactions'

    id = Column(String, primary_key=True)
    interaction_type = Column(String(50), nullable=False)
    interaction_date = Column(DateTime)
    notes = Column(String(255))

    contact = Column(String, ForeignKey('contacts.id'))


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(String, primary_key=True)
    sale_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    notes = Column(String(255))

    contact_id = Column(String, ForeignKey('contacts.id'))
