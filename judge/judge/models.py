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