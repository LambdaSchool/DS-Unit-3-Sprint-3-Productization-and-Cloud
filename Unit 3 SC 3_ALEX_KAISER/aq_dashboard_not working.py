# # OpenAQ Air Quality Dashboard with Flask."""
# from flask import Flask
# import openaq
# from flask_sqlalchemy import SQLAlchemy

# APP = Flask(__name__)
# APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# DB = SQLAlchemy(APP)

# # @APP.route('/')
# # def root():
# #     """Base view."""
# #     return 'TODO - part 2 and beyond!'

# class Record(DB.Model):
#     id = DB.Column(DB.Integer, primary_key=True)
#     datetime = DB.Column(DB.String(25))
#     value = DB.Column(DB.Float, nullable=False)

#     def __repr__(self):
#         return '<Time {} - Value {}>'.format(self.datetime, self.value)

# def get_openaq():
#     api = openaq.OpenAQ()
#     status, body = api.measurements(city='Los Angeles', parameter='pm25')
#     results = body['results']
#     return results

# def add_results(results):
#     DB.drop_all()
#     DB.create_all()
#     for result in results:
#         data = Record(datetime=result['date']['utc'], value=result['value'])
#         DB.session.add(data)
    
#     DB.session.commit()

# @APP.route('/')
# def root():
#     api = openaq.OpenAQ()
#     status, body = api.measurements(city='Los Angeles', parameter='pm25')
#     # utc_datetime = body['results'][1]['date']['utc']
#     # value = body['results'][1]['value']
#     # result = utc_datetime + "," +str(value)
#     # results = body['results'][:2]
#     # utc_datetime_value = []
#     # for result in results:
#     #     utc_datetime_value.append(str((result['date']['utc'],result['value'])))

#     #data = get_openaq()
#     #add_results(data)

#     filtered_results = Record.query.filter(Record.value > 10).all()

#     # return filtered_results
#     return str(filtered_results)
    
# @APP.route('/refresh')
# def refresh():
#     """Pull fresh data from Open AQ and replace existing data."""
#     DB.drop_all()
#     DB.create_all()
#     # TODO Get data from OpenAQ, make Record objects with it, and add to db
#     DB.session.commit()
#     return 'Data refreshed!'
