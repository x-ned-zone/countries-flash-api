import requests
import unittest
# import json
import App
from multiprocessing import Pool

BASE_URL = "http://127.0.0.1:5000/"


requiredFieldsErrorMsg = [{'name': 'Name of the country is required'},
                          {'currency': 'currency of the country is required'},
                          {'alpha2code': 'alpha 2 code of the country is required'},
                          {'alpha3code': 'alpha 3 code of the country is required'},
                          'Fetching: No countries exist!']


class TestCountryAPI(unittest.TestCase):
    def test_all_required_fields(self):
        addRsp = requests.post(BASE_URL + "country/1", {"name": "South Africa",
                                                        "alpha2code": "ZA", "alpha3code": "ZAF",  "currency": "South African Rand"})
        self.assertEqual(addRsp.status_code, 201)
        countryRecord = requests.get(BASE_URL + "country/1")
        self.assertEqual(countryRecord.status_code, 200)

    def test_missing_required_fields(self):
        addRsp = requests.post(BASE_URL + "country/2", {})
        self.assertIn(addRsp.json()['message'], requiredFieldsErrorMsg)
        countryRecord = requests.get(BASE_URL + "country/2")
        self.assertEqual(countryRecord.status_code, 404)

    def test_update_country_fields(self):
        # Add country for test
        addRsp = requests.post(BASE_URL + "country/3", {"name": "South Africa",
                                                        "alpha2code": "ZA", "alpha3code": "ZAF",  "currency": "South African Rand"})
        self.assertEqual(addRsp.status_code, 201)
        # Test update
        updateRsp = requests.put(BASE_URL + "country/3", {"name": "South Africa",
                                                          "currency": "South African Rand(ZAR)"})
        self.assertEqual(updateRsp.status_code, 202)
        # Check if update worked
        countryRecord = requests.get(BASE_URL + "country/3")
        self.assertEqual(countryRecord.status_code, 200)
        self.assertEqual(countryRecord.json()[
                         'currency'], "South African Rand(ZAR)")

    def test_delete_country(self):
        # Add country for test
        addRsp = requests.post(BASE_URL + "country/4", {"name": "South Africa",
                                                        "alpha2code": "ZA", "alpha3code": "ZAF",  "currency": "South African Rand"})
        self.assertEqual(addRsp.status_code, 201)
        # Test-Delete it
        deleteRsp = requests.delete(BASE_URL + "country/4")
        self.assertEqual(deleteRsp.status_code, 202)

        countryRecord = requests.get(BASE_URL + "country/4")
        self.assertEqual(countryRecord.status_code, 404)

    def test_filter_country_by_currency(self):
        # Add country for test
        requests.post(BASE_URL + "country/5", {"name": "South Africa",
                                               "alpha2code": "ZA", "alpha3code": "ZAF",  "currency": "South African Rand"})

        filteredGetRsp = requests.get(BASE_URL + "country/South African Rand")
        self.assertEqual(filteredGetRsp.status_code, 200)
        self.assertTrue(len(filteredGetRsp.json()) > 0)

    def test_filter_country_by_currency_not_found(self):
        filteredGetRsp = requests.get(BASE_URL + "country/USD")
        self.assertEqual(filteredGetRsp.status_code, 404)
        self.assertEqual(filteredGetRsp.json()[
                         'message'], 'Fetching: No countries exist!')

    def test_get_country_list(self):
        # Add country for test
        requests.post(BASE_URL + "country/6", {"name": "South Africa",
                                               "alpha2code": "ZA", "alpha3code": "ZAF",  "currency": "South African Rand"})

        countryRecordRsp = requests.get(BASE_URL + "country/all")
        self.assertEqual(countryRecordRsp.status_code, 200)
        self.assertGreater(len(countryRecordRsp.json()), 0)


if __name__ == "__main__":
    pool = Pool(processes=1)
    result = pool.apply_async(App.main)
    unittest.main()
    func = requests.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    pool.close()
