from decouple import config
from .models import DB, Measurement
from cityair import openaq

def load_measurement():
  api = openaq.OpenAQ()
  status, body = api.measurements(city='Los Angeles', parameter='pm25')
  if status == 200:
    try:
      for i in range(len(body['results'])):
        city = body['results'][i]['city']
        country = body['results'][i]['country']
        location = body['results'][i]['location']
        parameter = body['results'][i]['parameter']
        date_utc = body['results'][i]['date']['utc'][:10]
        date_local = body['results'][i]['date']['local'][:10]
        pm25 = body['results'][i]['value']
        unit = body['results'][i]['unit']
        latitude = body['results'][i]['coordinates']['latitude']
        longitude = body['results'][i]['coordinates']['longitude']

        db_measurement = Measurement(city=city,
                                       country=country, 
                                       location=location, 
                                       parameter=parameter, 
                                       date_utc=date_utc, 
                                       date_local=date_local, 
                                       pm25=pm25, 
                                       unit=unit, 
                                       latitude=latitude, 
                                       longitude=longitude )
        DB.session.add(db_measurement)
    except Exception as e:
       print('Error processing {}: {}'.format('loading measurement', e))
       raise e
    else:
       DB.session.commit()
       return status


def filter_ge_pm25(ge_pm25):
  measurement=Measurement.query.filter(Measurement.pm25 >= ge_pm25)
  return measurement
