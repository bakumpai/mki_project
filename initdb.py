from database import init_db as migrate
from database import seed

migrate()
seed()
