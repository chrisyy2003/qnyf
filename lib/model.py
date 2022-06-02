import peewee
from peewee import IntegerField, TextField, PrimaryKeyField

db = peewee.SqliteDatabase('data.db')

class Stu(peewee.Model):
    uid = IntegerField()
    name= TextField()
    number = TextField()
    info = TextField()
    sex = TextField()
    passwd = TextField()

    class Meta:
        database = db
        db_table = 'student'

class passcard(peewee.Model):
    name= TextField()
    number = TextField()
    passwd= TextField()
    endtime = TextField()
    count = IntegerField()

    class Meta:
        database = db
        db_table = 'passcard'

class account(peewee.Model):
    url= TextField(primary_key=True)
    count = IntegerField()
    lasttime = TextField()
    lefttime = IntegerField()
    testcount = IntegerField()
    test = IntegerField()

    class Meta:
        database = db
        db_table = 'account'

class daka(peewee.Model):
    yxdm = IntegerField()
    name= TextField()
    number = TextField(primary_key=True)
    passwd = TextField()
    loc = TextField()

    class Meta:
        database = db
        db_table = 'daka'




if __name__ == "__main__":
    pass