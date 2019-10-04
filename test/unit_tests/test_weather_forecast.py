import unittest
from weather_forecast import WeatherForecast


class TestWeatherForecast(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestWeatherForecast, self).__init__(*args, **kwargs)
        self.wf = WeatherForecast(open('..\..\key.txt', 'r').read())

    def _subtest_ok(self, data, name, country, city_id):
        self.assertEqual(data['name'], name)
        self.assertEqual(data['sys']['country'], country)
        self.assertEqual(data['id'], city_id)

        # It is not possible to compare some request data with determined
        # values. So it's enough to check necessary keys existence.
        self.assertTrue('description' in data['weather'][0])
        self.assertTrue('temp' in data['main'])

    def _subtest_not_found(self, data):
        self.assertFalse(data['ok'])
        self.assertEqual(data['message'].lower(), 'city not found')

    # Request by name
    def test_forecast_by_name_not_found(self):
        data = self.wf.forecast_by_name('asdfg13', '')
        self._subtest_not_found(data)

    def test_forecast_by_name_ok(self):
        name, country, city_id = 'London', 'GB', 2643743
        data = self.wf.forecast_by_name(name, country)
        self.assertTrue(data['ok'])
        self._subtest_ok(data, name, country, city_id)

    # Request by index
    def test_forecast_by_id_ok(self):
        name, country, city_id = 'Moscow', 'RU', 524901
        data = self.wf.forecast_by_id(city_id)
        self.assertTrue(data['ok'])
        self._subtest_ok(data, name, country, city_id)

    def test_forecast_by_id_not_found(self):
        data = self.wf.forecast_by_id(10)
        self._subtest_not_found(data)

    # Find request
    def test_forecast_from_find_request_single_res(self):
        name, country, city_id = 'London', 'GB', 2643743
        data = self.wf.forecast_from_find_request(name, country)
        self.assertTrue(data['ok'])
        self.assertEqual(data['count'], 1)
        self._subtest_ok(data['list'][0], name, country, city_id)

    def test_forecast_from_find_request_many_res(self):
        name = 'London'
        data = self.wf.forecast_from_find_request(name, '')
        self.assertTrue(data['ok'])
        self.assertGreater(data['count'], 1)

        def check_list_item(data_item, name):
            self.assertEqual(data_item['name'], name)
            self.assertTrue('country' in data_item['sys'])
            self.assertTrue('id' in data_item)
            self.assertTrue('description' in data_item['weather'][0])
            self.assertTrue('temp' in data_item['main'])

        for data_item in data['list']:
            check_list_item(data_item, name)

    def test_forecast_from_find_request_not_found(self):
        name = 'Moscow'
        data = self.wf.forecast_from_find_request(name, 'QW')
        self.assertTrue(data['ok'])
        self.assertEqual(data['count'], 0)
