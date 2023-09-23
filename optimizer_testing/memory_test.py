from memory_profiler import profile
import os
import pandas as pd
from lineup import Lineup_Rule
from slate import Slate



def read_slate_file(directory_path, file_name):
    # Check if the CSV file exists
    csv_file_path = os.path.join(directory_path, file_name + '.csv')
    if os.path.exists(csv_file_path):
        return pd.read_csv(csv_file_path)

    # Check if the XLSX file exists
    xlsx_file_path = os.path.join(directory_path, file_name + '.xlsx')
    if os.path.exists(xlsx_file_path):
        return pd.read_excel(xlsx_file_path)
    
    # Check if the XLS file exists
    xls_file_path = os.path.join(directory_path, file_name + '.xls')
    if os.path.exists(xls_file_path):
        return pd.read_excel(xls_file_path)
    
    # Check if the XLSM file exists
    xlsm_file_path = os.path.join(directory_path, file_name + '.xlsm')
    if os.path.exists(xlsm_file_path):
        return pd.read_excel(xlsm_file_path)

    # If neither CSV nor XLSX file exists, return None or raise an error
    return None








path = './'
file = 'Week3_Proj_DK'
new_slate_df=read_slate_file(path,file)
my_lineup_rule = Lineup_Rule(position_ordered_list=['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FLEX', 'DST'], flex_definitions={'FLEX': ['RB', 'TE', 'WR']}, salary_cap=50000)
week3_dk_main_slate=Slate(new_slate_df, slate_lineup_rule=my_lineup_rule)

path = './'
file = 'Week3_Proj_FD'
new_slate_df=read_slate_file(path,file)
my_lineup_rule = Lineup_Rule(position_ordered_list=['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FLEX', 'DST'], flex_definitions={'FLEX': ['RB', 'TE', 'WR']}, salary_cap=60000)
week3_fd_main_slate=Slate(new_slate_df, slate_lineup_rule=my_lineup_rule)

@profile
def run_boom_bust(n=1000, *slates:Slate):
    return_list=[]
    for slate in slates:
        slate.configure_optimization()
        opto=slate.calc_optimal_frequency(n=n)
        return_list.append(opto)
    return return_list


if __name__=='__main__':
    run_boom_bust(1000,week3_dk_main_slate,week3_fd_main_slate)

    