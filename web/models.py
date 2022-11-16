from peewee import *
from dotenv import load_dotenv
from database import db
import datetime

load_dotenv()

class BaseModel(Model):
    class Meta:
        database = db

class Sensor(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=100,unique=True)
    value = CharField(max_length=100)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')])

class Configs(BaseModel):
    id = AutoField(primary_key = True)
    name = CharField(max_length=100,unique=True)
    value = CharField(max_length=100)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')])