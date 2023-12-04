from database import Base
from sqlalchemy import Column, String

class Filter(Base):
    __tablename__ = "filters"
    
    id = Column(String(255), primary_key=True, index=True)  # Długość String musi być określona w MySQL
