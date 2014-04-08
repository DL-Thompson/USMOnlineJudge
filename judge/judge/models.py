from judge import app, db
from datetime import datetime
import flask.ext.whooshalchemy as whooshalchemy



class PageContent(db.Model):
    id = db.Column("ID", db.Integer, primary_key=True)
    page = db.Column("PAGE", db.String(60))
    content = db.Column("CONTENT", db.Text)

    def __init__(self, page, content):
        self.page = page
        self.content = content

    def __repr__(self):
        return '<PageContent %r>' % self.page

    def get_content(self):
        return self.content


class Exercises(db.Model):
    id = db.Column("ID", db.Integer, primary_key=True)
    title = db.Column("TITLE", db.String(60))
    difficulty = db.Column("DIFFICULTY", db.Integer)
    category = db.Column("CATEGORY", db.String(20))
    content = db.Column("CONTENT", db.Text)

    def __init__(self, title, difficulty, category, content):
        self.title = title
        self.difficulty = difficulty
        self.category = category
        self.content = content

    def __repr__(self):
        return '<Exercises %r>' % self.title


class User(db.Model):
    user_id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    primary_email = db.Column(db.String(120))
    profile = db.relationship('Profile', backref='user', lazy='dynamic')

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


class Profile(db.Model):
    __searchable__ = ['full_name', 'public_email', 'homepage', 'company', 'school', 'location']
    profile_id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    show_public = db.Column(db.Boolean, nullable=False)
    full_name = db.Column(db.String(120))
    public_email = db.Column(db.String(120))
    homepage = db.Column(db.String(256))
    company = db.Column(db.String(120))
    school = db.Column(db.String(120))
    location = db.Column(db.String(120))
    join_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'))

    def __init__(self, user):
        self.show_public = False
        self.join_date = datetime.utcnow()
        self.user_id = user.user_id
        self.full_name = ""
        self.public_email = ""
        self.homepage = ""
        self.company = ""
        self.school = ""
        self.location = ""

    def __repr__(self):
        return '<profile_id: %r> \n <show_public: %r> \n <full_name: %r> \n <public_email: %r> \n <homepage: %r> \n <company: %r> \n <school: %r> \n <location: %r> \n' \
               '<join_date: %r> \n <user_id: %r>' % (self.profile_id, self.show_public, self.full_name, self.public_email, self.homepage, self.company, self.school, self.location, self.join_date, self.user_id)

whooshalchemy.whoosh_index(app, Profile)


class Statistics(db.Model):
    statistic_id = db.Column("STATISTIC_ID", db.BigInteger, primary_key=True, autoincrement=True)
    profile_id = db.Column("PROFILE_ID", db.BigInteger, db.ForeignKey('profile.profile_id'))
    exercise_id = db.Column("EXERCISE_ID", db.Integer)
    time = db.Column("TIME", db.Integer)
    memory = db.Column("MEMORY", db.Integer)
    attempts = db.Column("ATTEMPTS", db.Integer)
    passed = db.Column("PASSED", db.Boolean)

    def __init__(self, profile_id, exercise_id, time, memory, passed):
        self.profile_id = profile_id
        self.exercise_id = exercise_id
        self.time = time
        self.memory = memory
        self.passed = passed

    def __repr__(self):
        return '<Statistic ID: %r>\n<Profile ID: %r>\n<Exercise ID: %r>\n<Time: %r>\n<Memory: %r>\n<Attempts: %r>\n<Passed: %r>' % (self.statistic_id, self.profile_id, self.exercise_id, self.time, self.memory, self.attempts, self.passed)
