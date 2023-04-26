from flask import Flask, jsonify
from faker import Faker
import itertools
from sqlalchemy import create_engine, text
import logging
import json

app = Flask(__name__)
faker = Faker()

logging.basicConfig(level=logging.DEBUG)
logging.debug("FAKER SERVICE INICIADO")

def execute_queries(list_queries_string=[], querie_type = ''):
    db_name = "rainbow_database"
    db_user = "unicorn_user"
    db_pass = "magical_password"
    db_host = "database-service"
    db_port = "5432"
    d = []
    try:
        db_string = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        db = create_engine(db_string)
        if querie_type == "INSERT":
            for querie in list_queries_string:
                with db.connect() as conn:
                    conn.execute(text(querie)).rowcount
                    conn.commit()
                    return {"message": "proceso ejecutado correctamente"}
        if querie_type == "SELECT":
            for querie in list_queries_string:
                with db.connect() as conn:
                    data_profiles = conn.execute(text(querie)).fetchall()
            # logging.debug(data_profiles)
            for ix in data_profiles:
                logging.debug(ix)
                # d.append
            return json.dumps([dict(ix) for ix in data_profiles])
            # return data_profiles
    except Exception as ex:
        logging.debug(f"Error: {ex}")

def random_data():
    try:
        insert_queries = []
        profiles = [dict(itertools.islice(faker.profile().items(), 6)) for data in range(13)]
        for profile in profiles:
            sql = ""
            for llave, valor in profile.items():
                if llave == "current_location":
                    coordinates = [str(coordinate) for coordinate  in valor]
                    profile.update(current_location = json.dumps({"coordinates": coordinates}))
            values = (str(list(profile.values())).replace("\\", "")[1:-1])
            sql = f"""
                INSERT INTO profile(job
                                    , company
                                    , ssn
                                    , residence
                                    , current_location
                                    , blood_group)
                VALUES ({values});
            """.replace("\n", "")
            insert_queries.append(sql)
        return insert_queries
    except Exception as ex:
        logging.error(ex)

@app.route("/crear_registros")
def create_profiels():
    try:
        data_profiles = random_data()
        resutls_querie = execute_queries(data_profiles, "INSERT")
        return resutls_querie
    except:
        return {"message": "error en el endpoint de crear registros"}
    
@app.route("/obtener_registros")
def get_profile():
    query_data = "SELECT * FROM profile;"
    try:
        data_profile = json.loads(
            execute_queries([query_data], "SELECT")
        )
        return json.dumps(str(data_profile))
    except Exception as ex:
        logging.error(ex)
        return {"message": "error en consulta de datos en servicio faker-service"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
