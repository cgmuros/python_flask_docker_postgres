from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

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

db_name = "rainbow_database"
db_user = "unicorn_user"
db_pass = "magical_password"
db_host = "localhost"
db_port = "5432"

db_string = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_string)

# conn =  engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

profiles = session.query(Profiles).all()

prof = dict_helper(profiles)
print(prof)