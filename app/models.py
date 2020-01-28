from app import db
from sqlalchemy import Column, Integer, String

class Sequence(db.Model):
    __tablename__="sequence"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    sequence = Column(String(10000), nullable=False)
    description = Column(String(10000), nullable=True)
    
    def __init__(self, name="", sequence="", description=""):
        self.name = name
        self.sequence = sequence
        self.description = description
    
    def __repr__(self):
        return '<Sequence {}>'.format(self.name)
