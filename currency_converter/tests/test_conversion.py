from decimal import Decimal
from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework.test import APIClient


class ConversionInputTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()
        self.converter = patch('api.views.convert').start()
        self.addCleanup(patch.stopall)
        self.converter.side_effect = (
            lambda source, target, amount: Decimal(amount) * 2
        )

    def assert_rejected(self, params):
        self.converter.reset_mock()
        response = self.client.get('/convert/', params)
        self.assertEqual(response.status_code, 400)
        self.converter.assert_not_called()

    def test_missing_parameters(self):
        complete = {'from': 'USD', 'to': 'EUR', 'amount': '2'}
        for missing in complete:
            with self.subTest(missing=missing):
                params = complete.copy()
                del params[missing]
                self.assert_rejected(params)
        self.assert_rejected({})

    def test_empty_parameters(self):
        for empty in ('from', 'to', 'amount'):
            with self.subTest(empty=empty):
                params = {'from': 'USD', 'to': 'EUR', 'amount': '2'}
                params[empty] = ''
                self.assert_rejected(params)

    def test_invalid_and_nonpositive_amounts(self):
        for amount in ('abc', '1,2,3', '0', '-1', '1e-999'):
            with self.subTest(amount=amount):
                self.assert_rejected({
                    'from': 'USD', 'to': 'EUR', 'amount': amount,
                })

    def test_nonfinite_amounts(self):
        for amount in ('NaN', 'nan', 'sNaN', 'Infinity', 'inf',
                       '-Infinity', '1e999'):
            with self.subTest(amount=amount):
                self.assert_rejected({
                    'from': 'USD', 'to': 'EUR', 'amount': amount,
                })

    def test_unknown_currencies(self):
        for field in ('from', 'to'):
            with self.subTest(field=field):
                params = {'from': 'USD', 'to': 'EUR', 'amount': '2'}
                params[field] = 'XYZ'
                self.assert_rejected(params)

    def test_supported_amount_formats(self):
        for amount, normalized in (('1,25', '1.25'), ('1.25', '1.25'),
                                   ('1e2', '1e2')):
            with self.subTest(amount=amount):
                params = {'from': 'usd', 'to': 'eur', 'amount': amount}
                response = self.client.get('/convert/', params)
                self.assertEqual(response.status_code, 200)
                self.converter.assert_called_with('USD', 'EUR', normalized)
                self.assertEqual(response.json()['info']['rate'], 2)
                self.assertEqual(response.json()['result'],
                                 float(Decimal(normalized) * 2))
                self.assertEqual(response.json()['query'], params)

    def test_finite_amount_with_overflowing_result_is_rejected(self):
        response = self.client.get('/convert/', {
            'from': 'USD', 'to': 'EUR', 'amount': '1e308',
        })
        self.assertEqual(response.status_code, 400)
        self.converter.assert_called_once_with('USD', 'EUR', '1e308')
        self.assertIn('Уменьшите сумму', response.json()[0])

    def test_large_json_safe_result_remains_supported(self):
        response = self.client.get('/convert/', {
            'from': 'USD', 'to': 'EUR', 'amount': '5e307',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 1e308)
        self.assertEqual(response.json()['info']['rate'], 2)
