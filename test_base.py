from app import db
from sqlalchemy.orm import relationship




class Bratuha(db.Model):
    __tablename__ = 'bratuhas'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(50))
    search_queries = relationship("Queries", backref="bratuha", lazy='dynamic')

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        #return unicode(self.id)
        return int(self.id)

    def __repr__(self):
        return "<User(login='%s', password='%s')>" % (self.login, self.password)



class Queries(db.Model):
    __tablename__ = 'queries'
    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String(50))
    bratuha_id = db.Column(db.Integer, db.ForeignKey('bratuhas.id'))
    #bratuha = relationship("Bratuha", back_populates="search_queries")

    def __init__(self, search_query, bratuha_id):
        self.search_query = search_query
        self.bratuha_id = bratuha_id




#user1 = Bratuha('Kolya', 'pass1')

#query1 = Queries('met', bratuha = user1)
#db.session.add(user1)
#db.session.add(query1)
#db.session.commit()

#res = Queries.query.filter(Queries.bratuha_id == '3')
#res = Queries.query.order_by(Queries.search_query).all()
#str(res.id)

#for instance in db.session.query(Queries).filter(Queries.bratuha_id == '3'):
 #   print(instance.id, instance.search_query, instance.bratuha_id)

for instance, br in db.session.query(Queries, Bratuha).filter(Queries.bratuha_id == '3').filter(Queries.bratuha_id == Bratuha.id):
    #print(instance.id, instance.search_query, instance.bratuha_id, br.login)
    print(instance.id, instance.search_query, instance.bratuha_id, br.login)

print('--------------------')

for instance, br in db.session.query(Queries, Bratuha).filter(Queries.search_query == 'rrrr').filter(Queries.bratuha_id == Bratuha.id):
    #print(instance.id, instance.search_query, instance.bratuha_id, br.login)
    print(instance.id, instance.search_query, instance.bratuha_id, br.login)

print('--------------------')

for user in db.session.query(Bratuha):
    print(user.login)
print('--------------------')

for user in db.session.query(Bratuha).filter(Bratuha.id == '2'):
    user1 = user.id
#user1 = db.session.query(Bratuha).filter(Bratuha.id == '2')
print(user1)

#print(res.id)




