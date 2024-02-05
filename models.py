from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class Category(Base):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Определение связи с таблицей News
    news = relationship('News', back_populates='category')

class Location(Base):
    __tablename__ = 'location'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    news = relationship('News', back_populates='location')
class Site(Base):
    __tablename__ = 'site'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)       

    news = relationship('News', back_populates='site')

class News(Base):
    __tablename__ = 'news'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(DateTime)
    content = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))  # Внешний ключ
    location_id = Column(Integer, ForeignKey('location.id'))
    site_id = Column(Integer, ForeignKey('site.id'))
    summarized_content = Column(String)
    old_id = Column(Integer)
    is_read = Column(Boolean)

    # Определение связи с таблицей Category
    # category = relationship('Category', back_populates='news')
    category = relationship('Category', back_populates='news', foreign_keys=[category_id])
    location = relationship('Location', back_populates='news')
    site = relationship('Site', back_populates='news')

    def set_category_id(self, category_id):
        self.category_id = category_id
