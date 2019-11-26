from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class TeachingAssistant(Base):
    __tablename__ = "teaching_assistant"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    course_ta = relationship("Course")

    def __init__(self, name = None):
        self.name = name


    def __repr__(self):
        return '<Teaching Assistant %r' % (self.name)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

