from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(255), primary_key=True, index=True)  # MySQL wymaga określenia długości dla String
    description = Column(Text, nullable=False)  # Użyto Text zamiast String dla potencjalnie długich opisów
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    status = Column(String(255), nullable=True)
    score = Column(String(255), nullable=True)
    scoreText = Column(String(255), nullable=True)
    is_acked = Column(Boolean, default=False)
    user = relationship("User", back_populates="acked_alerts")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    url = Column(Text, nullable=False)  # Jeśli URL może być długi, lepiej użyć Text
    notes = Column(Text, nullable=True)  # Podobnie jak w przypadku opisu, Text dla dłuższych notatek

    def __repr__(self):
        return f"<Alert {self.id}>"
