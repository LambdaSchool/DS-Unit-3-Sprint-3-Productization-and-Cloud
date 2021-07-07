import openaq
api = openaq.OpenAQ()
status, body = api.measurements(city='Los Angeles', parameters='pm25')

