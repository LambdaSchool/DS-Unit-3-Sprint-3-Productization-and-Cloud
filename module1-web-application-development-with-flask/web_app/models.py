from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author_id = db.Column(db.String(128))

    def __repr__(self):
        return f"<Book {self.id} {self.title}>"


# def parse_records(database_records):
#     """
#     A helper method for converting a list of database record objects into a list of dictionaries, so they can be returned as JSON

#     Param: database_records (a list of db.Model instances)

#     Example: parse_records(User.query.all())

#     Returns: a list of dictionaries, each corresponding to a record, like...
#         [
#             {"id": 1, "title": "Book 1"},
#             {"id": 2, "title": "Book 2"},
#             {"id": 3, "title": "Book 3"},
#         ]
#     """
#     parsed_records = []
#     for record in database_records:
#         print(record)
#         parsed_record = record.__dict__
#         del parsed_record["_sa_instance_state"]
#         parsed_records.append(parsed_record)
#     return parsed_records

class User(db.Model):
    """Twitter users corresponding to Tweets in the Tweet table."""
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    # Tweet IDs are ordinal ints, so can be used to fetch only more recent
    newest_tweet_id = db.Column(db.BigInteger)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Tweet(db.Model):
    """Tweets and their embeddings from Basilica."""
    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Unicode(300))  # Allowing for full + links
    embedding = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)
