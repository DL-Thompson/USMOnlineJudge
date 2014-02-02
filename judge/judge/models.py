from judge import app
from flask.ext.sqlalchemy import SQLAlchemy

import prod_cfg

usr = prod_cfg.user
pw = prod_cfg.password
server = prod_cfg.server
db_name = prod_cfg.db_name

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (usr, pw, server, db_name)
db = SQLAlchemy(app)


class PageContent(db.Model):
    __tablename__ = 'PageContent'

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
