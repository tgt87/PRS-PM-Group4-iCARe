# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.category_prediction import CategoryPrediction  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCoeController(BaseTestCase):
    """CoeController integration test stubs"""

    def test_get_coe_prediction_by_category(self):
        """Test case for get_coe_prediction_by_category

        Get COE prediction by category
        """
        query_string = [('category', 'category_example')]
        response = self.client.open(
            '/api/v1/coe/prediction',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
