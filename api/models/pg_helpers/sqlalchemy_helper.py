import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


class SqlalchemyHelper(object):
    engine = create_engine("postgres+psycopg2://postgres:postgres@code_challenge_postgres/postgres")

    SessionFactory = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

    if 'unittest' in sys.modules:
        connection = engine.connect()
        SessionFactory = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=connection)
    ########################################################

    session = scoped_session(SessionFactory)
    Base = declarative_base()
    Base.query = session.query_property()
    Base.session = session
