import requests
import json
from datetime import datetime

from model.weather_data import WeatherData


class WeatherForecast:
    def __init__(self):
        self.city = 'London'
        self.country = 'GB'
        self.weather_data = None
        self.temp_units = 'C'
        self.resp_error_msg = ''

    def get_forecast(self):
        '''
        :return: Response success (bool), and string message
        Weather forecast in string format:
        '<City>, <Date>, <Description>, <Temperature>'
        '''
        self.weather_data = self._parse_data_from_request()

        if self.weather_data:
            return True, ', '.join((self.city,
                              self.weather_data.date_str(),
                              self.weather_data.description,
                              str(self.weather_data.temp_c) + self.temp_units))
        else:
            # return False, 'Error message'
            return False, self.resp_error_msg

    def set_location(self, city, country):
        # TODO: Check names here
        self.city = city
        self.country = country

    def _url(self):
        return r'http://api.openweathermap.org/data/2.5/weather?q={city},' \
               r'{country}&appid=' \
               r'332aff71953e43412a946ab10190bc7a'.format(city=self.city,
                                                          country=self.country)

    def _http_request(self):
        url = self._url()
        try:
            return requests.get(url, stream=True, timeout=(10, 10))
        except requests.exceptions.ConnectTimeout:
            self.resp_error_msg = 'Connection timeout occurred! ' \
                                  'Please try later.'
            return None
        except requests.exceptions.ReadTimeout:
            self.resp_error_msg = 'Read timeout occurred! Please try later.'
            return None
        except requests.exceptions.ConnectionError:
            self.resp_error_msg = 'Connection failed. Please try later'
            return None
        except requests.exceptions.HTTPError:
            self.resp_error_msg = 'HTTP Error occurred.'
            return None
        except Exception as e:
            self.resp_error_msg = e
            return None

    def _parse_data_from_request(self):
        # TODO: check response
        response = self._http_request()
        if response is not None:
            data = json.loads(response.text)
            if response.ok:
                temp = data['main']['temp']
                descript = data['weather'][0]['description']
                return WeatherData(datetime.now(), temp, descript)
            else:
                self.resp_error_msg = data['message']
                return None
        else:
            return None


if __name__ == '__main__':
    wf = WeatherForecast()
    print(wf.get_forecast())
