from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import prod_cfg
import dev_cfg

production_env = True
if production_env:
    usr = prod_cfg.user
    pw = prod_cfg.password
    server = prod_cfg.server
    db_name = prod_cfg.db_name
else:
    usr = dev_cfg.user
    pw = dev_cfg.password
    server = dev_cfg.server
    db_name = dev_cfg.db_name

engine = create_engine('mysql://%s:%s@%s/%s' % (usr, pw, server, db_name), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
