from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'<Date: {self.datetime}, PPM: {self.value},'


