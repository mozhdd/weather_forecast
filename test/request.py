import requests
import json
from datetime import datetime
mock_file = r'weather.txt'

URL = r'http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=332' \
      r'aff71953e43412a946ab10190bc7a'


f = requests.get(URL)
tmp = f.text
data = json.loads(f.text)
data = json.load(open(mock_file, 'r'))


date = datetime.strftime(datetime.now(), "%a %d %b %Y %H:%M")
clouds = 'clouds {:d} %'.format(data['clouds']['all'])

t_k = data['main']['temp']
t_c = t_k - 273.15
temp = '{:d}C'.format(int(t_c))


print(', '.join(('London', date, clouds, temp)))
