from datetime import datetime


class WeatherData:
    def __init__(self, data):
        '''
        :param data: dict of weather forecast response data
        '''
        self.data = data
        self.date = datetime.now()
        self.temp_k = data['main']['temp']
        self.description = data['weather'][0]['description']
        self.city = data['name']
        self.country = data['sys']['country']
        self.city_id = data['id']

        self.temp_u = {'c': self.temp_c, 'f': self.temp_f}

    def get_str_weather(self, temp_units):
        return ', '.join((self.city,
                          self.country,
                          self.date_str(),
                          self.description,
                          str(self.temp_u[temp_units.lower()]) + temp_units))

    @property
    def temp_c(self):
        return round(self.temp_k - 273.15)

    @property
    def temp_f(self):
        return round(9/5 * self.temp_k - 459.67)

    def date_str(self, fmt="%a %d %b %Y %H:%M"):
        '''
        :return: <Weekday> <Day> <Month> <Year> <Hours>:<Min>
        '''
        return datetime.strftime(self.date, fmt)
