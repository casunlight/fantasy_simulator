# Create objects and methods related to a given slate. A slate is defined by which players are available, a set of games, salaries for all players, a contest type, a lineup rule, and a set of projections

from lineup import Lineup_Rule, Lineup
import pandas as pd
import numpy as np
import copy
from player import Slate_Player
from pulp import LpProblem, LpMaximize, LpVariable, lpSum



class Slate():
    def __init__(self, slate_df: pd.DataFrame, slate_lineup_rule: Lineup_Rule):
        required_cols = ['position', 'name + id', 'name', 'id', 'roster position', 'salary', 'game info', 'teamabbrev', 'proj', 'ownership', 'opponent']
        slate_total_players = slate_df.shape[0]
        #make everything lower case internally so that case doesn't matter going fwd
        df_cols = slate_df.columns.to_list()
        for i in range(len(df_cols)):
            df_cols[i]=df_cols[i].lower()
        slate_df.columns = df_cols
        missing_cols=[]
        for col in required_cols:
            if col.lower() not in df_cols:
                missing_cols.append(col)
        if len(missing_cols)>0:
            raise ValueError('Missing the following required columns: ' + str(missing_cols))
        else:
            print('DataFrame has all required columns, new Slate object successfully completed')

        #initialize object data
        self.slate_df = slate_df
        self.slate_lineup_rule = slate_lineup_rule
        #initalize Numpy arrays for faster calculation. Numpy arrays are faster than Pandas series objects
        self.name_array = np.array(self.slate_df['name'])
        self.id_array = np.array(self.slate_df['id'])
        self.name_id_array = np.array(self.slate_df['name + id'])
        self.position_array = np.array(self.slate_df['position'])
        self.roster_position_array = np.array(self.slate_df['roster position'])
        self.salary_array = np.array(self.slate_df['salary'])
        self.game_info_array = np.array(self.slate_df['game info'])
        self.teamabbrev_array = np.array(self.slate_df['teamabbrev'])
        self.proj_array = np.array(self.slate_df['proj'])
        self.ownership_array = np.array(self.slate_df['ownership'])
        self.opponent_array = np.array(self.slate_df['opponent'])
        if 'stdev' not in self.slate_df.columns.to_list():
            self.stdev_array = np.zeros(self.proj_array.shape)
            self.slate_df['stdev'] = self.stdev_array
        else:
            self.stdev_array = np.array(self.slate_df['stdev'])
        
        #initialize arrays for just the optimizer's use, so that you dont lose original data about projection, etc
        self._opto_proj_array = copy.deepcopy(self.proj_array)
        self._opto_stdev_array = copy.deepcopy(self.stdev_array)
        self._opto_gametime_array = copy.deepcopy(self.game_info_array)
        
        #There has to be a better way to do this
        var_names=[]
        for i in range(slate_total_players):
            var_names.append(str(self.position_array[i]) + '_' + str(self.id_array[i]))
        self._opto_var_names = np.array(var_names)
        
        #Initialize a list of slate_player objects so that later work is faster and easier
        slate_player_list = []
        for i in range(slate_total_players):
            slate_player_list.append(Slate_Player(name=self.name_array[i], slate_name_id=self.name_id_array[i], position=self.position_array[i], var_name=self._opto_var_names[i], game_time=self._opto_gametime_array[i], base_proj=self.proj_array[i], percent_own=self.ownership_array[i], stdev=self.stdev_array[i]))
        self.slate_player_array = np.array(copy.deepcopy(slate_player_list))


    def __str__(self):
        return str(self.slate_df)
    
    def __repr__(self):
        return str(self.slate_df)
    
    def configure_optimization(self):
        #Do all the optimizer stuff that doesn't need to be repeated every time you call the solver
        self._optimizer_LpProblem = LpProblem('maximize', LpMaximize)
        self._optimizer_salary_cap = self.slate_lineup_rule.salary_cap
        self._optimizer_total_players = self.slate_lineup_rule.total_players
        self._optimizer_players_per_position = self.slate_lineup_rule.players_per_posn
        self._optimizer_flex_eligibility = self.slate_lineup_rule.flex_definitions


        #NEED TO FIX THIS FOR THE NEW DATA FORMAT
        #Here we convert lineup rules into something the LpSolver will understand
        self._optimizer_position_constraint_equal_to = {k:v for k, v in self._optimizer_players_per_position.items() if (k not in self._optimizer_flex_eligibility['FLEX'] and k!='FLEX')}
        if 'FLEX' in self._optimizer_players_per_position.keys():
            self._optimizer_position_constraint_greater_than = {k:v for k, v in self._optimizer_players_per_position.items() if (k in self._optimizer_flex_eligibility['FLEX'] and k!='FLEX')}
            self._optimizer_position_constraint_less_than = {k:v+1 for k, v in self._optimizer_players_per_position.items() if (k in self._optimizer_flex_eligibility['FLEX'] and k!='FLEX')}

        #local variable for creating dictionaries by position
        availables = self.slate_df.groupby(['position','id','name + id','proj','salary']).agg('count').reset_index()
        salaries_by_position = {}
        projections_by_position = {}
        #Create a dictionaries by position for both salary and projection
        for pos in availables.position.unique():
            available_by_position = availables[availables.position==pos]
            salaries_by_position[pos] = list(available_by_position[['id', 'salary']].set_index('id').to_dict().values())[0]
            projections_by_position[pos] = list(available_by_position[['id', 'proj']].set_index('id').to_dict().values())[0]

        _vars = {k: LpVariable.dict(k, v, cat='Binary') for k, v in projections_by_position.items()}#Changed v from a proj to an LpVariable
        rewards=[]
        costs=[]
        for k, v in _vars.items():
            costs += lpSum([salaries_by_position[k][i] * _vars[k][i] for i in v])
            rewards += lpSum([projections_by_position[k][i] * _vars[k][i] for i in v])
            if k in self._optimizer_position_constraint_equal_to:
                self._optimizer_LpProblem += lpSum([_vars[k][i] for i in v]) == self._optimizer_position_constraint_equal_to[k]
            if k in self._optimizer_position_constraint_less_than:
                self._optimizer_LpProblem += lpSum([_vars[k][i] for i in v]) <= self._optimizer_position_constraint_less_than[k]
            if k in self._optimizer_position_constraint_greater_than:
                self._optimizer_LpProblem += lpSum([_vars[k][i] for i in v]) >= self._optimizer_position_constraint_greater_than[k]

        total_players_constraint = lpSum([v.values() for v in _vars.values()]) == self._optimizer_total_players
        self._optimizer_LpProblem += total_players_constraint
        salary_cap_constraint = lpSum(costs) <= self._optimizer_salary_cap
        self._optimizer_LpProblem += salary_cap_constraint
        objective = lpSum(rewards)#no constraint so will be treated like the objective 
        self._optimizer_LpProblem += objective
        
        #Create a numpy array of optimization binary variables so it's easy to reset the objective quickly
        opto_bin_var=[]
        for i in range(self.id_array.shape[0]):
            var=_vars[self.position_array[i]][self.id_array[i]]
            opto_bin_var.append(var)
        self._opto_bin_var=np.array(opto_bin_var)

    def reset_optimizer_objective(self):
        new_objective=[]
        for i in range(self._opto_proj_array.shape[0]):
            new_objective+=lpSum(self._opto_bin_var[i]*self._opto_proj_array[i])
        self._optimizer_LpProblem.objective = new_objective 

    def calc_optimal_lineup(self):
        self._optimizer_LpProblem.solve()
        lineup_players=[]
        for _var in self._optimizer_LpProblem.variables():
            if _var.value()==1:
                index = np.where(self._opto_var_names==_var.name)[0][0]
                lineup_players.append(self.slate_player_array[index])
        return Lineup(lineup_players, self.slate_lineup_rule)

    def simulate_slate(self, apply_to_opto=True):
        sim = np.random.normal(self.proj_array, self.stdev_array)
        if apply_to_opto:
            self._opto_proj_array = sim
            self.reset_optimizer_objective()
        return sim#Maybe shouldnt return anything

    def calc_optimal_frequency(self, n=1000):
        opto_percent_array = np.zeros(self._opto_proj_array.shape,dtype=float)
        for sim in range(n):
            self.simulate_slate(apply_to_opto=True)
            optimal_lineup = self.calc_optimal_lineup()
            #There has to be a faster way
            for j in range(opto_percent_array.shape[0]):
                if self.slate_player_array[j] in optimal_lineup.players:
                    opto_percent_array[j] += 1
        opto_percent_array=100*opto_percent_array/n


        boom_bust_df=pd.DataFrame({'Name':self.name_array,'Name_id':self.name_id_array,'Team':self.teamabbrev_array,'Opponent':self.opponent_array,'Position':self.position_array,'MedianProj':self.proj_array,'StDev':self.stdev_array,'Optimal%':opto_percent_array,'Ownership':self.ownership_array,'Leverage':opto_percent_array-self.ownership_array})
        boom_bust_df.to_excel('BoomBustProbability.xlsx',index=False)
        return boom_bust_df
    
    def produce_simulated_opto_lineups(self, n=1000):
        lineup_list=[]
        for sim in range(n):
            self.simulate_slate(apply_to_opto=True)
            optimal_lineup=self.calc_optimal_lineup()
            optimal_lineup.sort_player_list()
            lineup_list.append(optimal_lineup)
        return lineup_list
    










class Slatev2():
    def __init__(self, slate_df:pd.DataFrame, site:str='DRAFTKINGS', sport:str='NFL', contest_type:str='CLASSIC'):





        required_cols = ['position', 'name + id', 'name', 'id', 'roster position', 'salary', 'game info', 'teamabbrev', 'proj', 'ownership', 'opponent']
        slate_total_players = slate_df.shape[0]
        #make everything lower case internally so that case doesn't matter going fwd
        df_cols = slate_df.columns.to_list()
        for i in range(len(df_cols)):
            df_cols[i]=df_cols[i].lower()
        slate_df.columns = df_cols
        missing_cols=[]
        for col in required_cols:
            if col.lower() not in df_cols:
                missing_cols.append(col)
        if len(missing_cols)>0:
            raise ValueError('Missing the following required columns: ' + str(missing_cols))
        else:
            print('DataFrame has all required columns, new Slate object successfully completed')

        #initialize object data
        self.slate_df = slate_df
        self.slate_lineup_rule = slate_lineup_rule
        #initalize Numpy arrays for faster calculation. Numpy arrays are faster than Pandas series objects
        self.name_array = np.array(self.slate_df['name'])
        self.id_array = np.array(self.slate_df['id'])
        self.name_id_array = np.array(self.slate_df['name + id'])
        self.position_array = np.array(self.slate_df['position'])
        self.roster_position_array = np.array(self.slate_df['roster position'])
        self.salary_array = np.array(self.slate_df['salary'])
        self.game_info_array = np.array(self.slate_df['game info'])
        self.teamabbrev_array = np.array(self.slate_df['teamabbrev'])
        self.proj_array = np.array(self.slate_df['proj'])
        self.ownership_array = np.array(self.slate_df['ownership'])
        self.opponent_array = np.array(self.slate_df['opponent'])
        if 'stdev' not in self.slate_df.columns.to_list():
            self.stdev_array = np.zeros(self.proj_array.shape)
            self.slate_df['stdev'] = self.stdev_array
        else:
            self.stdev_array = np.array(self.slate_df['stdev'])
        
        #initialize arrays for just the optimizer's use, so that you dont lose original data about projection, etc
        self._opto_proj_array = copy.deepcopy(self.proj_array)
        self._opto_stdev_array = copy.deepcopy(self.stdev_array)
        self._opto_gametime_array = copy.deepcopy(self.game_info_array)
        
        #There has to be a better way to do this
        var_names=[]
        for i in range(slate_total_players):
            var_names.append(str(self.position_array[i]) + '_' + str(self.id_array[i]))
        self._opto_var_names = np.array(var_names)
        
        #Initialize a list of slate_player objects so that later work is faster and easier
        slate_player_list = []
        for i in range(slate_total_players):
            slate_player_list.append(Slate_Player(name=self.name_array[i], slate_name_id=self.name_id_array[i], position=self.position_array[i], var_name=self._opto_var_names[i], game_time=self._opto_gametime_array[i], base_proj=self.proj_array[i], percent_own=self.ownership_array[i], stdev=self.stdev_array[i]))
        self.slate_player_array = np.array(copy.deepcopy(slate_player_list))


    def __str__(self):
        return str(self.slate_df)
    
    def __repr__(self):
        return str(self.slate_df)
    
    def configure_optimization(self):
        #Do all the optimizer stuff that doesn't need to be repeated every time you call the solver
        self._optimizer_LpProblem = LpProblem('maximize', LpMaximize)
        self._optimizer_salary_cap = self.slate_lineup_rule.salary_cap
        self._optimizer_total_players = self.slate_lineup_rule.total_players
        self._optimizer_players_per_position = self.slate_lineup_rule.players_per_posn
        self._optimizer_flex_eligibility = self.slate_lineup_rule.flex_definitions


        #NEED TO FIX THIS FOR THE NEW DATA FORMAT
        #Here we convert lineup rules into something the LpSolver will understand
        self._optimizer_position_constraint_equal_to = {k:v for k, v in self._optimizer_players_per_position.items() if (k not in self._optimizer_flex_eligibility['FLEX'] and k!='FLEX')}
        if 'FLEX' in self._optimizer_players_per_position.keys():
            self._optimizer_position_constraint_greater_than = {k:v for k, v in self._optimizer_players_per_position.items() if (k in self._optimizer_flex_eligibility['FLEX'] and k!='FLEX')}
            self._optimizer_position_constraint_less_than = {k:v+1 for k, v in self._optimizer_players_per_position.items() if (k in self._optimizer_flex_eligibility['FLEX'] and k!='FLEX')}

        #local variable for creating dictionaries by position
        availables = self.slate_df.groupby(['position','id','name + id','proj','salary']).agg('count').reset_index()
        salaries_by_position = {}
        projections_by_position = {}
        #Create a dictionaries by position for both salary and projection
        for pos in availables.position.unique():
            available_by_position = availables[availables.position==pos]
            salaries_by_position[pos] = list(available_by_position[['id', 'salary']].set_index('id').to_dict().values())[0]
            projections_by_position[pos] = list(available_by_position[['id', 'proj']].set_index('id').to_dict().values())[0]

        _vars = {k: LpVariable.dict(k, v, cat='Binary') for k, v in projections_by_position.items()}#Changed v from a proj to an LpVariable
        rewards=[]
        costs=[]
        for k, v in _vars.items():
            costs += lpSum([salaries_by_position[k][i] * _vars[k][i] for i in v])
            rewards += lpSum([projections_by_position[k][i] * _vars[k][i] for i in v])
            if k in self._optimizer_position_constraint_equal_to:
                self._optimizer_LpProblem += lpSum([_vars[k][i] for i in v]) == self._optimizer_position_constraint_equal_to[k]
            if k in self._optimizer_position_constraint_less_than:
                self._optimizer_LpProblem += lpSum([_vars[k][i] for i in v]) <= self._optimizer_position_constraint_less_than[k]
            if k in self._optimizer_position_constraint_greater_than:
                self._optimizer_LpProblem += lpSum([_vars[k][i] for i in v]) >= self._optimizer_position_constraint_greater_than[k]

        total_players_constraint = lpSum([v.values() for v in _vars.values()]) == self._optimizer_total_players
        self._optimizer_LpProblem += total_players_constraint
        salary_cap_constraint = lpSum(costs) <= self._optimizer_salary_cap
        self._optimizer_LpProblem += salary_cap_constraint
        objective = lpSum(rewards)#no constraint so will be treated like the objective 
        self._optimizer_LpProblem += objective
        
        #Create a numpy array of optimization binary variables so it's easy to reset the objective quickly
        opto_bin_var=[]
        for i in range(self.id_array.shape[0]):
            var=_vars[self.position_array[i]][self.id_array[i]]
            opto_bin_var.append(var)
        self._opto_bin_var=np.array(opto_bin_var)

    def reset_optimizer_objective(self):
        new_objective=[]
        for i in range(self._opto_proj_array.shape[0]):
            new_objective+=lpSum(self._opto_bin_var[i]*self._opto_proj_array[i])
        self._optimizer_LpProblem.objective = new_objective 

    def calc_optimal_lineup(self):
        self._optimizer_LpProblem.solve()
        lineup_players=[]
        for _var in self._optimizer_LpProblem.variables():
            if _var.value()==1:
                index = np.where(self._opto_var_names==_var.name)[0][0]
                lineup_players.append(self.slate_player_array[index])
        return Lineup(lineup_players, self.slate_lineup_rule)

    def simulate_slate(self, apply_to_opto=True):
        sim = np.random.normal(self.proj_array, self.stdev_array)
        if apply_to_opto:
            self._opto_proj_array = sim
            self.reset_optimizer_objective()
        return sim#Maybe shouldnt return anything

    def calc_optimal_frequency(self, n=1000):
        opto_percent_array = np.zeros(self._opto_proj_array.shape,dtype=float)
        for sim in range(n):
            self.simulate_slate(apply_to_opto=True)
            optimal_lineup = self.calc_optimal_lineup()
            #There has to be a faster way
            for j in range(opto_percent_array.shape[0]):
                if self.slate_player_array[j] in optimal_lineup.players:
                    opto_percent_array[j] += 1
        opto_percent_array=100*opto_percent_array/n

        
        boom_bust_df=pd.DataFrame({'Name':self.name_array,'Name_id':self.name_id_array,'Team':self.teamabbrev_array,'Opponent':self.opponent_array,'Position':self.position_array,'MedianProj':self.proj_array,'StDev':self.stdev_array,'Optimal%':opto_percent_array,'Ownership':self.ownership_array,'Leverage':opto_percent_array-self.ownership_array})
        boom_bust_df.to_excel('BoomBustProbability.xlsx',index=False)
        return boom_bust_df
    
    def produce_simulated_opto_lineups(self, n=1000):
        lineup_list=[]
        for sim in range(n):
            self.simulate_slate(apply_to_opto=True)
            optimal_lineup=self.calc_optimal_lineup()
            optimal_lineup.sort_player_list()
            lineup_list.append(optimal_lineup)
        return lineup_list