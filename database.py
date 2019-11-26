import json

from os import getcwd
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

# engine = create_engine('postgresql://postgres:satrio1234S@localhost/rce', convert_unicode=True)
engine = create_engine('sqlite:///' + getcwd() + '/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import user
    import teaching_assistant
    import course
    Base.metadata.create_all(bind=engine)


def seed():
    from user import User
    from teaching_assistant import TeachingAssistant
    from course import Course

    ta_names = ['Joko', 'Anwar', 'Budiman', 'Ujaja']
    courses = ['CS266 Spring', 'CS277 Winter', 'CS299 Fall', 'CS922 Kemarau']

    objects = list()

    for idx in range(len(ta_names)):
        objects.append(TeachingAssistant(ta_names[idx]))
        objects.append(Course(courses[idx], 2019, idx + 1))

    for name in ['satrio', 'nugroho', 'lengkap']:
        objects.append(User(name, name + '@example.com'))

    db_session.bulk_save_objects(objects)

    db_session.commit()


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields

        return json.JSONEncoder.default(self, obj)


def encoder(result):
    return json.dumps(result, cls=AlchemyEncoder)
