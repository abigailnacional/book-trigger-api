from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Book(Base):
    '''The Book class corresponds to the "books" database table.'''
    __tablename__ = 'books'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String)
    authors = Column(String)
    genres = Column(String)
    triggers = Column(String)
    age_group = Column(String)
    published = Column(String)
    publisher = Column(String)
