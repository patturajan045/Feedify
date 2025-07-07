from mongoengine import StringField,DateTimeField,ReferenceField,Document, CASCADE
from datetime import datetime
from uuid import uuid4

class Role(Document):
    meta = {"collection":"role"}   
      
    id = StringField(primary_key = True, default = lambda:str(uuid4()))
    name = StringField(required =True)
    addedTime =DateTimeField(default = datetime.now())
    updatedtime = DateTimeField()