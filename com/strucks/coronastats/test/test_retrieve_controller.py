# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from com.strucks.coronastats.models.overview_data_row import OverviewDataRow  # noqa: E501
from com.strucks.coronastats.test import BaseTestCase


class TestRetrieveController(BaseTestCase):
    """RetrieveController integration test stubs"""

    def test_current(self):
        """Test case for current

        Get Current
        """
        query_string = [('location', 'location_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/current',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_getsince(self):
        """Test case for getsince

        Your GET endpoint
        """
        query_string = [('location', 'location_example'),
                        ('days', 3.4)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/getsince',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
