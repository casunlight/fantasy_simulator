import pandas as pd
from django.core.management.base import BaseCommand
#from nfl.models import Player
#import numpy as np
import json
import copy
import os



class Command(BaseCommand):

    help="A command to convert excel or csv data to json in preparation for storage to our database"

    def handle(self, *args, **options):

        csv_file_path = './slate_csv/'
        csv_file_name = 'week1_main_slate.csv'
        csv_file = csv_file_path + csv_file_name
        #this file will always be called from root project directory (dir with manage.py)

        json_file_path = './slate_json/'
        json_file_name = csv_file_name
        json_file = json_file_path + json_file_name

        df = pd.read_csv(csv_file)

        df.columns = [column.lower() for column in df.columns]
        df.rename(columns={'name + id': 'name_id', 'game info': 'game_info'}, inplace=True)
        #df['model'] = 'player_app.player'

        print('\n*3')

        print(df)

        # Convert each row into a dictionary
        list_of_dicts = []
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            list_of_dicts.append(row_dict)

        #print(list_of_dicts)

        
        hi=False
        if hi:
            keys_to_nest = []

            for dict in list_of_dicts:
                old_dict = copy.deepcopy(dict)
                for k in keys_to_nest:
                    dict.pop(k)
                nested_info = {key: old_dict[key] for key in keys_to_nest}
                dict['fields'] = nested_info

            #print(list_of_dicts)
            with open(json_file_path, 'w') as json_file:
                json.dump(list_of_dicts, json_file, indent=4)  # indent for pretty formatting

            print("JSON data has been saved to:", json_file_path)
        else:
            pass