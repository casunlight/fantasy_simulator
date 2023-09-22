import pandas as pd
from django.core.management.base import BaseCommand
from nfl.models import Player
import numpy as np
import json
import copy
import os



class Command(BaseCommand):

    help="A command to add data from an Excel file to the database"

    def handle(self, *args, **options):

        #Add slate data from pga csv file to the database

        excel_file = './slate_excel/dk_nfl_main_slate.xlsx'
        file_path = './slate_json/dk_nfl_main_slate.json'

        current_directory = os.getcwd()
        print("Current working directory:", current_directory)

        df = pd.read_excel(excel_file)

        df.columns = [column.lower() for column in df.columns]
        df_sleek = df[['name','name + id', 'salary','position', 'proj']]
        df_sleek['model'] = 'nfl.player'
        new_order = ['model','name','name + id', 'salary','position', 'proj']
        final_df = df_sleek[new_order]

        #Change name + id to name_id since cant call a field name + id
        final_df.rename(columns={'name + id': 'name_id'}, inplace=True)

        # Convert each row into a dictionary
        list_of_dicts = []
        for index, row in final_df.iterrows():
            row_dict = row.to_dict()
            list_of_dicts.append(row_dict)

        keys_to_nest = ['name','name_id', 'salary', 'position', 'proj']

        for dict in list_of_dicts:
            old_dict = copy.deepcopy(dict)
            for k in keys_to_nest:
                dict.pop(k)
            nested_info = {key: old_dict[key] for key in keys_to_nest}
            dict['fields'] = nested_info

        #print(list_of_dicts)
        with open(file_path, 'w') as json_file:
            json.dump(list_of_dicts, json_file, indent=4)  # indent for pretty formatting

        print("JSON data has been saved to:", file_path)