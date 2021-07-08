from app_test import User
from app_test import db

# creating records?
db.create_all()
admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')

# add records
db.session.add(admin)
db.session.add(guest)
db.session.commit()
print(User.query.all())
print(User.query.filter_by(username='admin').first())
