from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///testbd.sqlite', echo=True)

Base = declarative_base()



class Bratuha(Base):
    __tablename__ = 'bratuhas'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    #def get_id(self):
        #return unicode(self.id)


    def __repr__(self):
        return "<User(login='%s', password='%s')>" % (self.login, self.password)


DBSession = sessionmaker(bind=engine)
session = DBSession()

#new_bratuha = Bratuha(login='Kolia', password='123')
#session.add(new_bratuha)
#session.commit()