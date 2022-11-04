import sys
import os
import connexion
import six

ROOT_DIR = os.path.abspath(os.curdir)
sys.path.insert(0, ROOT_DIR)

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.car import Car  # noqa: E501
from swagger_server.models.car_preference import CarPreference  # noqa: E501
from swagger_server import util
from swagger_server.services import car_services


def get_car_by_id(id):  # noqa: E501
    """Get car by Id

     # noqa: E501

    :param id: Id of car to retrieve
    :type id: int

    :rtype: Car
    """
    return 'do some magic!'


def suggest_cars_by_user_preference(body):  # noqa: E501
    """Suggest cars based on user car preference

     # noqa: E501

    :param body: User car preference
    :type body: dict | bytes

    :rtype: List[Car]
    """
    if connexion.request.is_json:
        body = CarPreference.from_dict(connexion.request.get_json())  # noqa: E501

    recommended_cars_list = car_services.get_recommended_cars(body)

    return recommended_cars_list
