from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class PumpData(Base):
    __tablename__ = 'pump_data'

    imei = Column(String, primary_key=True)  
    daily_water_discharge = Column(Float, default=0)
    cumulative_water_discharge = Column(Float, default=0)
    day_run_hours = Column(Float, default=0)
    cumulative_run_hours = Column(Float, default=0)
    cumulative_energy_generated = Column(Float, default=0)
    run_status = Column(Integer, default=0) 

DATABASE_URL = "postgresql://username:password@localhost/mydatabase"


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


new_pump_data = PumpData(imei="123456789012345", run_status=1)  # Example with run_status as integer

session.add(new_pump_data)
session.commit()

# Close the session
session.close()

print("Table created and data inserted successfully!")
