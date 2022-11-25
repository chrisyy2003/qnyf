import peewee
from peewee import IntegerField, TextField

db = peewee.SqliteDatabase('./data/data.db')

class daka(peewee.Model):
    yxdm = IntegerField()
    name = TextField()
    number = TextField(primary_key=True)
    passwd = TextField()
    loc = TextField()

    class Meta:
        database = db
        db_table = 'daka'

db.connect()
db.create_tables([daka])
