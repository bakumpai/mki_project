from sqlalchemy import Column, Integer, String, ForeignKey


from database import Base

class CourseWithAssistantObj(object):
    def __init__(self, course, teaching_assistant):
        self.id = course.id
        self.name = course.name
        self.year = course.year
        self.teaching_assistant = teaching_assistant


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    year = Column(Integer)
    teaching_assistant_id = Column(Integer, ForeignKey('teaching_assistant.id'))


    def __init__(self, name = None, year = None, teaching_assistant = None):
        self.name = name
        self.year = year
        self.teaching_assistant_id = teaching_assistant

    def __repr_(self):
        return '<Course %r>' % (self.name)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
