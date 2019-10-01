import requests
import json

url = r'http://api.openweathermap.org/data/2.5/find?q=Moscow' \
      r'&appid=332aff71953e43412a946ab10190bc7a'

response = requests.get(url)

data = json.loads(response.text)

data['count']

for loc in data['list']:
    print(loc['name'], end=', ')
    print(loc['sys']['country'], end='. ')
    print('Geo coords ' + str(list(loc['coord'].values())))

locations = []
for loc in data['list']:
    locations.append('{0}, {1}. Geo coords {2}'.format(
        loc['name'], loc['sys']['country'], str(list(loc['coord'].values()))
    ))



locations = ['{0}, {1}. Geo coords {2}'.format(
    loc['name'], loc['sys']['country'],
    str(list(loc['coord'].values()))) for loc in data['list']]
