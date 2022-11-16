from peewee import *
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

db = MySQLDatabase(os.environ.get('DATABASE_NAME'), user=os.environ.get('DATABASE_USER'), 
            password=os.environ.get('DATABASE_PASS'), host=os.environ.get('DATABASE_HOST'), 
            port=int(os.environ.get('DATABASE_PORT')))

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