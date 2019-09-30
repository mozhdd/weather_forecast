import requests
import json


url = r'http://api.openweathermap.org/data/2.5/weather?q=moscow,us&appid=332' \
      r'aff71953e43412a946ab10190bc7a'

response = None
try:
    response = requests.get(url, stream=True, timeout=(10, 10))
    # return response
except requests.exceptions.ConnectTimeout:
    print('Oops. Connection timeout occured!')
except requests.exceptions.ReadTimeout:
    print('Oops. Read timeout occured')
except requests.exceptions.ConnectionError:
    print('Seems like dns lookup failed..')

except requests.exceptions.HTTPError as err:
    print('Oops. HTTP Error occured')
    print(
        'Response is: {content}'.format(content=err.response.content))
except Exception as e:
    print(e)

print(response)
data = json.loads(response.text)
# print(response.text)
print(data)

print(response.ok)
