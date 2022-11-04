import sys
import os
import pandas as pd
import json

#os.chdir('..\..')
ROOT_DIR = os.path.abspath(os.curdir)
sys.path.insert(0, ROOT_DIR)

from swagger_server.models.car import Car

def get_recommended_cars(body):
    '''
    Returns a list of Car objects recommended based on user's budget, preference for brand, type and purchase period
    '''
    # get input parameters
    startYear = body.start_year
    startMonth = body.start_month
    endYear = body.end_year
    endMonth = body.end_month
    brand_list = body.brand
    type_list = body.type
    budget = body.budget

    ## load car_prices.csv to get car info
    cars_filepath = '\data\car_prices.csv'
    cars_folderpath = ROOT_DIR + cars_filepath
    df = pd.read_csv(cars_folderpath)
    
    # get forecasted coe prices from json file
    coe_price_predictions = get_predictions()

    ## get forecast prices for COE category selected
    coe_price_predictions_category = coe_price_predictions[0]['series']

    ## filter coe_price_forecast for prices that are within user selected time period 
    bidding_exercises_selected = get_bidding_exercises(startYear, startMonth, endYear, endMonth) # get list of indexes    
    
    # get indexes for first and last bidding exercises
    first_bidding_exercise_selected = bidding_exercises_selected[0]
    last_bidding_exercise_selected = bidding_exercises_selected[-1]
    first_idx = 0
    final_idx = 0
    for idx, exercise in enumerate(coe_price_predictions_category):
        if coe_price_predictions_category[idx]['name'] == first_bidding_exercise_selected:
            first_idx = idx
        if coe_price_predictions_category[idx]['name'] == last_bidding_exercise_selected:
            final_idx = idx
    if final_idx != 0:
        predictions_for_period_selected = coe_price_predictions_category[first_idx:final_idx+1]
    else:
        predictions_for_period_selected = coe_price_predictions_category[first_idx:]
    

    # Search for the best bidding exercise(lowest COE prices
    best_bidding_exercise = '' 
    lowest_coe_price = 1000000
    for idx, _ in enumerate(predictions_for_period_selected):
        value = predictions_for_period_selected[idx]['value']
        
        if value < lowest_coe_price:
            best_bidding_exercise = predictions_for_period_selected[idx]['name']
            lowest_coe_price = value

    # Add column for price after coe    
    df.loc[:, 'price_after_coe'] = df.loc[:, 'price'] + lowest_coe_price

    # Filter df based on budget, brand, type selected
    if len(brand_list) == 0:
        brand_list = df['brand'].unique()
    if len(type_list) == 0:
        type_list = df['type'].unique()

    filtered_df = df[(df['brand'].isin(brand_list)) & (df['type'].isin(type_list)) & (df['price_after_coe'] <= budget)].sort_values('price_after_coe').reset_index(drop=True)
    print(filtered_df)
    ## Instantiate list to hold Car objects
    cars_list = []
    # populate Car object
    for i in range(filtered_df.shape[0]):
        car = Car()
        car.id = str(i)
        car.brand = filtered_df.loc[i, 'brand']
        car.model = filtered_df.loc[i, 'model']
        car.variant = filtered_df.loc[i, 'variant']
        car.type = filtered_df.loc[i, 'type']
        car.price_before_coe = filtered_df.loc[i, 'price']
        car.price_after_coe = filtered_df.loc[i, 'price_after_coe']
        car.best_bidding_exercise = best_bidding_exercise
        car.photo = filtered_df.loc[i, 'photo']
        cars_list.append(car) # append car object to list
    
    cars_list_json = json.loads(str(cars_list).replace("'", '"'))
    
    return cars_list_json

def get_predictions():
    # load forecasted coe prices from json file and return it
    with open('data/coe_prices.json', 'r') as f:
        coe_prices = json.load(f)
    
    return coe_prices


def get_bidding_exercises(startYear, startMonth, endYear, endMonth):
    # convert all strings to integers
    int_to_month_dict = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    month_to_int_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    start_year_int = int(startYear)
    end_year_int = int(endYear)
    start_month_int = month_to_int_dict[startMonth]
    end_month_int = month_to_int_dict[endMonth]

    # get number of bidding exercises: exercise_count
    exercise_count = 0
    if end_year_int == start_year_int:
        if end_month_int >= start_month_int:
            # get number of bidding exercises
            exercise_count = (end_month_int - start_month_int + 1) * 2 # 2 bidding exercises per month            
        else:
            return [] 
    elif end_year_int > start_year_int:
        # get number of bidding exercises
        exercise_count = ((13 - start_month_int) + ((end_year_int - start_year_int - 1) * 12) + end_month_int) * 2 # first year + n number of years + final year

    # generate list of indexes based on exercise_count
    month = start_month_int
    year = start_year_int
    next_bidding_exercise = 1
    index = []
    for i in range(exercise_count):
        month_string = int_to_month_dict[month]
        year_string = str(year)
        bidding_exercise_string = str(next_bidding_exercise)
        index_string = month_string + ' ' + year_string + ' (' + bidding_exercise_string + ')'
        index.append(index_string)

        # change values for next bidding exercise
        if next_bidding_exercise == 2:
            next_bidding_exercise = 1
            if month == 12: 
                month = 1
                year += 1
            elif month < 12:
                month += 1
        elif next_bidding_exercise == 1:
            next_bidding_exercise = 2

    return index

# cars_filepath = '\data\car_prices.csv'
# cars_folderpath = ROOT_DIR + cars_filepath
# df = pd.read_csv(cars_folderpath)
# brand_list = ['Honda', 'Kia']
# type_list = ['Sedan', 'SUV']
# filtered_df = df[(df['brand'].isin(brand_list)) & (df['type'].isin(type_list))].reset_index(drop=True)
# print(filtered_df)
# # get forecasted coe prices from json file
# coe_price_predictions = get_predictions()

# ## get forecast prices for COE category selected
# coe_price_predictions_category = coe_price_predictions['series']
# print(coe_price_predictions_category)



# body = {
#     "startYear":"2023", 
#     "startMonth":"Oct", 
#     "endYear":"2024", 
#     "endMonth":"Apr", 
#     "brand":['Honda', 'Kia'], 
#     "type":['Sedan', 'SUV'], 
#     "budget":200000
# }

# cars_list = get_recommended_cars(body)
# print(cars_list)