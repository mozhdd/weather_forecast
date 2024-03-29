import requests
import json


class WeatherForecast:
    def __init__(self, appid):
        self.appid = appid
        self.city = 'London'
        self.country = 'GB'
        self.temp_units = 'C'
        self.resp_error_msg = ''
        self.req_timeout = (10, 10)

    def forecast_by_name(self, city, country):
        self.set_location(city, country)
        response = self._http_request(self._url(method='weather'))

        return self._parse_data_from_response(response)

    def forecast_by_id(self, city_id):
        response = self._http_request(self._url(method='weather', id=city_id))

        return self._parse_data_from_response(response)

    def forecast_from_find_request(self, city, country):
        self.set_location(city, country)
        response = self._http_request(self._url(method='find'))

        return self._parse_data_from_response(response)

    def set_location(self, city, country):
        # TODO: Check names here
        self.city = city
        self.country = country

    def _url(self, method='weather', id=None):
        '''
        :param method: 'weather' returns forecast in one location
        'find' returns result of search cities with same names with different
        locations that also contains forecast for each
        :return: url string
        '''
        country = ','+self.country if self.country else self.country
        if id is None:
            query = 'q={city}{country}'.format(city=self.city, country=country)
        else:
            query = 'id={0}'.format(str(id))

        return r'http://api.openweathermap.org/data/2.5/{method}?{query}' \
               r'&appid={appid}'.format(method=method,
                                        query=query,
                                        appid=self.appid)

    def _http_request(self, url):
        try:
            return requests.get(url, stream=True, timeout=self.req_timeout)
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

    def _parse_data_from_response(self, response):
        '''
        :return: dict: {'ok': request validity,
                        'message': string responce message,
                        keys with data if request is ok}
        '''
        if response is not None:
            data = json.loads(response.text)
            if response.ok:
                data['ok'] = True
                return data
            else:
                # Mostly 'City not found'
                data['ok'] = False  # Set 'ok' flag if forecast is valid
                return data
        else:
            data = {'ok': False,
                    'message':  'Request failed. ' + self.resp_error_msg}
            return data


if __name__ == '__main__':
    wf = WeatherForecast(open('key.txt', 'r').read())
    data = wf.forecast_by_name('asdfg13', '')
    data = wf.forecast_by_name('London', 'GB')
    data = wf.forecast_by_name('London', '')

    data = wf.forecast_by_id(524901)
    data = wf.forecast_by_id(10)
    data = wf.forecast_by_id('asfsdf')

    data = wf.forecast_from_find_request('London', 'GB')
    data = wf.forecast_from_find_request('London', '')
    data = wf.forecast_from_find_request('Moscow', 'QW')
