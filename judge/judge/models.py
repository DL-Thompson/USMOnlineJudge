from judge import app
from database import Base
from sqlalchemy import Column, Integer, String, Text


class PageContent(Base):
    __tablename__ = 'PageContent'

    id = Column("ID", Integer, primary_key=True)
    page = Column("PAGE", String(60))
    content = Column("CONTENT", Text)

    def __init__(self, page, content):
        self.page = page
        self.content = content

    def __repr__(self):
        return '<PageContent %r>' % self.page

    def get_content(self):
        return self.content


class Exercises(Base):
    __tablename__ = 'Exercises'

    id = Column("ID", Integer, primary_key=True)
    title = Column("TITLE", String(60))
    difficulty = Column("DIFFICULTY", Integer)
    category = Column("CATEGORY", String(20))
    content = Column("CONTENT", Text)

    def __init__(self, title, difficulty, category, content):
        self.title = title
        self.difficulty = difficulty
        self.category = category
        self.content = content

    def __repr__(self):
        return '<Exercises %r>' % self.title


class User(Base):
    __tablename__ = "User"
    email = Column(String(120), primary_key=True)
    first_name = Column(String(64))
    last_name = Column(String(64))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.email)

    def __repr__(self):
        return '<Login: %r>' % (self.email)
