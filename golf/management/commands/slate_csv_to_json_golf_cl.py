import pandas as pd
from django.core.management.base import BaseCommand
from golf.models import Golfer
import numpy as np
import json
import copy


class Command(BaseCommand):
    help="A command to add data from an Excel file to the database"
    def handle(self, *args, **options):
        #Add slate data from pga csv file to the database

        excel_file = './slate_excel/golf_slate.xlsx'
        file_path = './dk_pga_slate_classic.json'


        df = pd.read_excel(excel_file)
        #print(df)


        df.columns = [column.lower() for column in df.columns]
        df_sleek = df[['name','name + id', 'salary', 'proj']]
        df_sleek['model'] = 'golf.golfer'
        new_order = ['model','name','name + id','salary','proj']
        final_df = df_sleek[new_order]

        #Change name + id to name_id since cant call a field name + id
        final_df.rename(columns={'name + id': 'name_id'}, inplace=True)

        # Convert each row into a dictionary
        list_of_dicts = []
        for index, row in final_df.iterrows():
            row_dict = row.to_dict()
            list_of_dicts.append(row_dict)

        print(list_of_dicts)
        print('\n'*2)

        keys_to_nest = ['name','name_id', 'salary', 'proj']

        for dict in list_of_dicts:
            old_dict = copy.deepcopy(dict)
            for k in keys_to_nest:
                dict.pop(k)
            nested_info = {key: old_dict[key] for key in keys_to_nest}
            dict['fields'] = nested_info

        print(list_of_dicts)

        with open(file_path, 'w') as json_file:
            json.dump(list_of_dicts, json_file, indent=4)  # indent for pretty formatting

        print("JSON data has been saved to:", file_path)

