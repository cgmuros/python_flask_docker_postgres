from flask import Flask, jsonify
from faker import Faker
import itertools
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker
import logging
import json

app = Flask(__name__)
faker = Faker()

logging.basicConfig(level=logging.DEBUG)
logging.debug("FAKER SERVICE INICIADO")

Base = declarative_base()

class Profiles(Base):
    __tablename__ = 'profile'

    id = Column(Integer(), primary_key=True)
    job = Column(String(150), nullable=False)
    company = Column(String(150), nullable=True)
    ssn = Column(String(), nullable=True)
    residence = Column(String(), nullable=True)
    current_location = Column(JSON(), nullable=True)
    blood_group = Column(String(), nullable=True)

    def obj_to_dict(self):  # for build json format
        return {
            "id": self.id,
            "job": self.job,
            "company": self.company,
            "ssn": self.ssn,
            "residence": self.residence,
            "current_location": self.current_location,
            "blood_group": self.blood_group
        }

def dict_helper(objlist):
    result2 = [item.obj_to_dict() for item in objlist]
    return result2

def execute_queries(list_queries_string=[], querie_type = ''):
    db_name = "rainbow_database"
    db_user = "unicorn_user"
    db_pass = "magical_password"
    db_host = "database-service"
    db_port = "5432"
    try:
        db_string = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(db_string)

        Session = sessionmaker(bind=engine)
        session = Session()
    
        if querie_type == "INSERT":
            for querie in list_queries_string:
                prof = Profiles(
                    job = querie['job'],
                    company = querie['company'],
                    ssn = querie['ssn'],
                    residence = querie['residence'],
                    current_location = querie['current_location'],
                    blood_group = querie['blood_group']
                )

                session.add(prof)
                session.commit()

            return {"message": "proceso ejecutado correctamente"}
        if querie_type == "SELECT":
            data_profiles = session.query(Profiles).all()
            profiles = dict_helper(data_profiles)
            res = json.dumps(profiles)
            return res
    except Exception as ex:
        logging.debug(f"Error: {ex}")

def random_data():
    try:
        # insert_queries = []
        profiles = [dict(itertools.islice(faker.profile().items(), 6)) for data in range(13)]
        
        for profile in profiles:
            for llave, valor in profile.items():
                if llave == "current_location":
                    coordinates = [str(coordinate) for coordinate  in valor]
                    profile.update(current_location = json.dumps({"coordinates": coordinates}))
                    profile.update(current_location = str(profile[llave]).replace("\\", ""))
            
        return profiles

    except Exception as ex:
        logging.error(ex)

@app.route("/crear_registros")
def create_profiels():
    try:
        data_profiles = random_data()
        resutls_querie = execute_queries(data_profiles, "INSERT")
        logging.debug(resutls_querie)
        return resutls_querie
        # return data_profiles
    except:
        return {"message": "error en el endpoint de crear registros"}
    
@app.route("/obtener_registros")
def get_profile():
    query_data = "SELECT * FROM profile;"
    try:
        data_profile = json.loads(
            execute_queries([query_data], "SELECT")
        )
        return json.dumps(data_profile)
    except Exception as ex:
        logging.error(ex)
        return {"message": "error en consulta de datos en servicio faker-service"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
