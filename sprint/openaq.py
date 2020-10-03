import requests

def get_tup():
    r = requests.get('https://api.openaq.org/v1/measurements?city=Los Angeles&parameter=pm25')
    data = r.json()
    l = []
    i = 0
    while i < 100:
        utc1 = data['results'][i]['date']['utc']
        val1 = data['results'][i]['value']
        tup = tuple([utc1,val1])
        l.append(tup)
        i+=1

    return l

if __name__ == '__main__':
    print(get_tup())