#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_cors import CORS
import os
import sys
from swagger_server.services import coe_services

ROOT_DIR = os.path.abspath(os.curdir)
sys.path.insert(0, ROOT_DIR)

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    CORS(app.app)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'iCARE - An Intelligent Car Budgeting Assistant'}, pythonic_params=True)
    app.run(port=8080)
    



if __name__ == '__main__':
    category_predictions_json = coe_services.generate_predictions(category="Category A", num_forecast=48, look_back=36, model_mape=6.8, historical_count=48)
    print('coe_services executed')
    main()
    
