from faker_sqlalchemy import SqlAlchemyProvider
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base
from faker import Faker

fake = Faker()
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


fake.add_provider(SqlAlchemyProvider)

instance = fake.sqlalchemy_model(Profiles)

print(instance.value)