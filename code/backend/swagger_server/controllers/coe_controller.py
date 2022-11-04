import os
import sys
import json

ROOT_DIR = os.path.abspath(os.curdir)
sys.path.insert(0, ROOT_DIR)

from flask import jsonify
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.category_prediction import CategoryPrediction # noqa: E501
from swagger_server import util
from swagger_server.services import coe_services

def get_coe_prediction_by_category(category):  # noqa: E501
    """Get COE prediction by category

     # noqa: E501

    :param category: Category that need to be considered for filter
    :type category: str

    :rtype: List[CategoryPrediction]
    """
    ## Read dataset and get predictions
    category_predictions_json = coe_services.get_predictions()
    
    return category_predictions_json
