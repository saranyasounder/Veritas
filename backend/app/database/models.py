from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# base class that all database models inherit from
# sqlalchemy uses this to track all tables
Base = declarative_base()

class Evaluation(Base):
    """
    Stores the result of each evaluation run.
    One row per evaluation — includes prompt, response, and all metric scores.
    """
    __tablename__ = 'evaluations'

    # auto incrementing primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # the input prompt sent to the model
    prompt = Column(Text, nullable=False)
    
    # model identifier e.g. 'anthropic/claude-sonnet-4'
    model = Column(String(300), nullable=False)
    
    # the model's generated response
    response = Column(Text, nullable=False)
    
    # all metric scores stored as JSON
    # e.g. {"BLEU": {"score": 0.8}, "ROUGE": {"score": 0.7}}
    metrics = Column(JSON, nullable=True)
    
    # when the evaluation was run
    timestamp = Column(DateTime, default=datetime.now)