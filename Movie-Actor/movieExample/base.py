from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:1234@localhost:3306/moviedb')

Session = sessionmaker(bind=engine)

Base = declarative_base()
