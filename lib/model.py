import peewee
from peewee import IntegerField, TextField

db = peewee.SqliteDatabase('data.db')


class Stu(peewee.Model):
    uid = IntegerField()
    name = TextField()
    number = TextField()
    info = TextField()
    sex = TextField()
    passwd = TextField()

    class Meta:
        database = db
        db_table = 'student'


class daka(peewee.Model):
    yxdm = IntegerField()
    name = TextField()
    number = TextField(primary_key=True)
    passwd = TextField()
    loc = TextField()

    class Meta:
        database = db
        db_table = 'daka'


if __name__ == "__main__":
    pass
