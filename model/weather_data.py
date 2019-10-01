from datetime import datetime


class WeatherData:
    def __init__(self, date, temp_k, description, city, country):
        '''
        Stores necessary weather data in appropriate format
        :param date: Curent date (datetime.datetime)
        :param temp_k: Temperature in Kelvin(float)
        :param description: weather description (string)
        '''
        self.date = date
        self.temp_k = temp_k
        self.description = description
        self.city = city
        self.country = country

        self.temp_u = {'c': self.temp_c, 'f': self.temp_f}

    def get_str_weather(self, temp_units):
        return ', '.join((self.city,
                          self.country,
                          self.date_str(),
                          self.description,
                          str(self.temp_u[temp_units.lower()]) + temp_units))

    @property
    def temp_c(self):
        return int(self.temp_k - 273.15)

    @property
    def temp_f(self):
        return int(9/5 * self.temp_k - 459.67)

    def date_str(self, fmt="%a %d %b %Y %H:%M"):
        '''
        :return: <Weekday> <Day> <Month> <Year> <Hours>:<Min>
        '''
        return datetime.strftime(self.date, fmt)
