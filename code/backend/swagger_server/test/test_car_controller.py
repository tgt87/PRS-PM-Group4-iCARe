# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.car import Car  # noqa: E501
from swagger_server.models.car_preference import CarPreference  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCarController(BaseTestCase):
    """CarController integration test stubs"""

    def test_get_car_by_id(self):
        """Test case for get_car_by_id

        Get car by Id
        """
        response = self.client.open(
            '/api/v1/cars/{id}'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_suggest_cars_by_user_preference(self):
        """Test case for suggest_cars_by_user_preference

        Suggest cars based on user car preference
        """
        body = CarPreference()
        response = self.client.open(
            '/api/v1/cars/suggest',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
