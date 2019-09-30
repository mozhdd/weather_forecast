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
            return False, 'Error message'

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
        return requests.get(url)

    def _parse_data_from_request(self):
        # TODO: check response
        response = self._http_request()
        if response:
            data = json.loads(response.text)
            temp = data['main']['temp']
            descript = data['weather'][0]['description']

            return WeatherData(datetime.now(), temp, descript)
        else:
            return None


if __name__ == '__main__':
    wf = WeatherForecast()
    print(wf.get_forecast())
