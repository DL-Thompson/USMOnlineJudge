from judge import app
from database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, BigInteger, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


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
    user_id = Column(BigInteger, autoincrement=True, primary_key=True)
    primary_email = Column(String(120))
    profile = relationship('Profile', backref='owner', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.primary_email)

    def __repr__(self):
        return '<Login: %r>' % (self.primary_email)


class Profile(Base):
    __tablename__ = "Profile"
    profile_id = Column(BigInteger, autoincrement=True, primary_key=True)
    show_public = Column(Boolean, nullable=False)
    full_name = Column(String(120))
    public_email = Column(String(120))
    homepage = Column(String(256))
    company = Column(String(120))
    school = Column(String(120))
    location = Column(String(120))
    join_date = Column(DateTime, nullable=False)
    user_id = Column(BigInteger, ForeignKey('User.user_id'))

    def __init__(self, user):
        self.show_public = False
        self.join_date = datetime.utcnow()
        self.user_id = user.user_id

    def __repr__(self):
        return '<profile_id: %r> \n <show_public: %r> \n <full_name: %r> \n <public_email: %r> \n <homepage: %r> \n <company: %r> \n <school: %r> \n <location: %r> \n' \
               '<join_date: %r> \n <user_id: %r>' % (self.profile_id, self.show_public, self.full_name, self.public_email, self.homepage, self.company, self.school, self.location, self.join_date, self.user_id)
