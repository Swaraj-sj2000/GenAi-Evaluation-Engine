#app/models/run.py

from sqlalchemy import Boolean, Column,Integer,String,Float,DateTime, func
from app.database import Base

class Run(Base):
    __tablename__='runs'
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, nullable=False)
    prompt = Column(String, nullable=False)
    model_output = Column(String, nullable=False)
    model_name = Column(String, default="gpt-4")
    status = Column(String, default="pending")
    score = Column(Float, nullable=True)
    correctness=Column(Float,nullable=True)
    completeness=Column(Float,nullable=True)
    clarity=Column(Float,nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    is_golden = Column(Boolean, default=False)  
    expected_score = Column(Float, nullable=True)


    

    