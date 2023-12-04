from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)  # Długość String musi być określona
    password = Column(String(255), nullable=False)  # Długość String dla bezpieczeństwa haseł
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    permissions = Column(Integer, default=0)
    acked_alerts = relationship("Alert", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"
