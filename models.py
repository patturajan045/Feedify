from mongoengine import StringField,DateTimeField,ReferenceField,Document, CASCADE, EmailField
from datetime import datetime
from uuid import uuid4

class Role(Document):
    meta = {"collection":"role"}   
      
    id = StringField(primary_key = True, default = lambda:str(uuid4()))
    name = StringField(required =True)
    addedTime =DateTimeField(default = datetime.now())
    updatedtime = DateTimeField()

class User(Document):
    meta = {"collection" : "user"}
    
    id = StringField(primary_key = True, default = lambda : str(uuid4()))
    name = StringField(required = True)
    email = EmailField(required = True, unique = True)
    phone = StringField(required = True)
    role = ReferenceField(Role, required = True, reverse_delete_rule=CASCADE, null = True)
    password = StringField(required = True)
    addedTime = DateTimeField(default = datetime.now())
    updatedTime = DateTimeField()