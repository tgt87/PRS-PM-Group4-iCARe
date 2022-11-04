# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.predictions import Predictions  # noqa: F401,E501
from swagger_server import util

import json
from json import JSONEncoder



class CategoryPrediction(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, series: List[Predictions]=None):  # noqa: E501
        """CategoryPrediction - a model defined in Swagger

        :param name: The name of this CategoryPrediction.  # noqa: E501
        :type name: str
        :param series: The series of this CategoryPrediction.  # noqa: E501
        :type series: List[Predictions]
        """
        self.swagger_types = {
            'name': str,
            'series': List[Predictions]
        }

        self.attribute_map = {
            'name': 'name',
            'series': 'series'
        }
        self._name = name
        self._series = series

    @classmethod
    def from_dict(cls, dikt) -> 'CategoryPrediction':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CategoryPrediction of this CategoryPrediction.  # noqa: E501
        :rtype: CategoryPrediction
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this CategoryPrediction.


        :return: The name of this CategoryPrediction.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this CategoryPrediction.


        :param name: The name of this CategoryPrediction.
        :type name: str
        """
        allowed_values = ["Category A", "Category B", "Category C", "Category D", "Category E"]  # noqa: E501
        if name not in allowed_values:
            raise ValueError(
                "Invalid value for `name` ({0}), must be one of {1}"
                .format(name, allowed_values)
            )

        self._name = name

    @property
    def series(self) -> List[Predictions]:
        """Gets the series of this CategoryPrediction.


        :return: The series of this CategoryPrediction.
        :rtype: List[Predictions]
        """
        return self._series

    @series.setter
    def series(self, series: List[Predictions]):
        """Sets the series of this CategoryPrediction.


        :param series: The series of this CategoryPrediction.
        :type series: List[Predictions]
        """

        self._series = series