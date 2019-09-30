from datetime import datetime


class WeatherData:
    def __init__(self, date, temp_k, clouds):
        '''
        Stores necessary weather data in appropriate format
        :param date: Curent date (datetime.datetime)
        :param temp_k: Temperature in Kelvin(float)
        :param clouds: Clouds percentage(int)
        '''
        self.date = date
        self.temp_k = temp_k
        self.clouds = clouds

    @property
    def temp_c(self):
        return int(self.temp_k - 273.15)

    def temp_f(self):
        return int(9/5 * self.temp_k - 459.67)

    def date_str(self, fmt="%a %d %b %Y %H:%M"):
        '''
        :return: <Weekday> <Day> <Month> <Year> <Hours>:<Min>
        '''
        return datetime.strftime(self.date, fmt)
