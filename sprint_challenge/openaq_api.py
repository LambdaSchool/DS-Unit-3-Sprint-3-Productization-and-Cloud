import openaq


def get_aq_data():
    # Import and set up the API object
    api = openaq.OpenAQ()

    # Retrieve the data from the API when the main route is called
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    # Create a list of tuples of (utc_datetime, value)
    data_tup_list = []
    for data in body['results']:
        tup = (data['date']['utc'], data['value'])
        data_tup_list.append(tup)

    # Return this list in the main route, 
    #so loading the web application prints the raw list of tuples of datetimes and values
    return data_tup_list