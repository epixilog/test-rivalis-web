from sanic import Sanic
from sanic import response
from sanic.response import redirect
from app.blueprints import Blueprints
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import json   
import config

from sqlalchemy.inspection import inspect


# helper class
class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]




# todo  move this to models 

#Creating model table for our CRUD database
class student(Base , Serializer):
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    prenom = sqlalchemy.Column(sqlalchemy.String(length=50))
    nom = sqlalchemy.Column(sqlalchemy.String(length=50))
    birthDate = sqlalchemy.Column(sqlalchemy.String(length=10))
    mark_1 = sqlalchemy.Column(sqlalchemy.Integer)
    mark_2 = sqlalchemy.Column(sqlalchemy.Integer)
    mark_3 = sqlalchemy.Column(sqlalchemy.Integer)


 
    def serialize(self):
        d = Serializer.serialize(self)
        return d


# create the web app

app = Sanic(__name__)

# todo add all fo the api to blueprints 

# app.blueprint(Blueprints.auth, url_prefix='app/blueprints/blueprint')


# Define the MySQL engine using MySQL Connector/Python

# todo change this to private variable 
engine = sqlalchemy.create_engine(
    'mysql+mysqlconnector://student0:Maro@1270@localhost:3306/sqlalchemy',
    echo=True)
 


 # Define and create the table
Base = declarative_base()

Base.metadata.create_all(engine)
 
# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()
 

# This is the index route where we are going to
# query on all our students

@app.route('/')
async def Index(req):
    our_user = session.query(student).all()
        # Serializing json    
    json_object = json.dumps([student.serialize(m) for m in our_user])  
        
    return response.json(json_object)
 

#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
async def insert(request):
 
    if request.method == 'POST':
 
        prenom = request.form['prenom']
        nom = request.form['nom']
        birthDate = request.form['birthDate']
        mark_1  = request.form['mark_1']
        mark_2 = request.form['mark_2']
        mark_3 = request.form['mark_3']



        student_ = student(prenom, nom , birthDate , mark_1, mark_2, mark_3)

        count  = session.query(student).filter(student.nom == student_.nom ).count()
        if count > 0:
            print ('user exists')
        else : 
            session.add(student_)
            session.commit()
 
        # prompt ' inserted succecfully'  vuejs prompts ?!
        url = app.url_for('Index')
        return redirect(url)
 
 
#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
async def update(request):
 
    if request.method == 'POST':
        data = session.query.get(request.form.get('id'))
 
        data.prenom = request.form['prenom']
        data.nom = request.form['nom']
        data.birthDate = request.form['birthDate']
        data.mark_1  = request.form['mark_1']
        data.mark_2 = request.form['mark_2']
        data.mark_3 = request.form['mark_3']
 
        session.commit()
        
        # prompt ("student Updated Successfully")
        url = app.url_for('Index')

        return redirect(url)
  
 
 
# #This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    data = session.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
 
    return redirect(url_for('Index'))


  

if __name__ == '__main__':
    app.go_fast(port=config.PORT, workers=config.WORKERS,
                debug=config.DEBUG)