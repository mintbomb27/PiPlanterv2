from contextvars import ContextVar
import peewee
from peewee import *
from dotenv import load_dotenv
import os

load_dotenv()

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())

class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]

db = MySQLDatabase(os.environ.get('DATABASE_NAME'), user=os.environ.get('DATABASE_USER'), 
            password=os.environ.get('DATABASE_PASS'), host=os.environ.get('DATABASE_HOST'), 
            port=int(os.environ.get('DATABASE_PORT')))

db._state = PeeweeConnectionState()