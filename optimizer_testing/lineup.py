
from player import Slate_Player
import copy



class Lineup_Rule():
    def __init__(self, position_ordered_list: list[str], flex_definitions: dict, salary_cap: int, score_mult: dict=None, salary_mult: dict=None):
        self.lineup_order=position_ordered_list
        self.flex_definitions = flex_definitions
        self.salary_cap = salary_cap
        self.score_mult = score_mult#For example, if a CPTN accrues 1.5x his underlying player's points, give {'CPTN':1.5}, else leave blank
        self.salary_mult = salary_mult#For example, if a CPTN costs 1.5x his underlying player's salary, give {'CPTN':1.5}, else leave blank
        self.total_players = len(position_ordered_list)
        players_per_posn={}
        for posn in self.lineup_order:
            if posn not in players_per_posn.keys():
                players_per_posn[posn] = 1
            else:
                players_per_posn[posn] = players_per_posn[posn] + 1
        self.players_per_posn = players_per_posn

        
        #Determine min and max native positions, just need to determine how many flex positions each native position is eligible for
        #First, determine which positions in players_per_posn are actually flex. Create a new dict without this flex, only native
        native_dict=copy.deepcopy(self.players_per_posn)
        flex_pos=[]
        for k, v in native_dict.items():
            if k in flex_definitions.keys():
                flex_pos.append(k)
        
        for key in flex_pos:
            native_dict.pop(key)

        self.position_min_dict=native_dict
        max_dict=copy.deepcopy(native_dict)
        for k, v in max_dict.items():
            for k_, val in flex_definitions.items():
                if k in val:
                    max_dict[k] = max_dict[k] + 1
        self.position_max_dict=max_dict


    def __str__(self):
        return str(self.lineup_order)

    def __repr__(self):
        return str(self.lineup_order)
    





class Lineup():
    def __init__(self, players: list[Slate_Player], lineup_rule: Lineup_Rule):
        self.players = players#A list of slate_player objects
        base_proj=0
        sum_ownership=0
        for player in self.players:
            base_proj+=player.base_proj
            sum_ownership+=player.percent_own
        self.base_proj = base_proj
        self.sum_ownership = sum_ownership
        self.lineup_rule = lineup_rule
        self.lineup_sim_score=0

    def __str__(self):
        return str(self.players)
    
    def __repr__(self):
        return str(self.players)
    
    def __eq__(self, other):
        if isinstance(other, Lineup):
            for player in other.players:
                if player not in self.players:
                    return False
            return True
        return False
        

    def calc_simulated_score(self):
        sim_score=0
        for player in self.players:
            sim_score+=player._sim_score
        self.lineup_sim_score=sim_score
        

    def sort_player_list(self):
        position_output_order = self.lineup_rule.lineup_order
        flex_definitions = self.lineup_rule.flex_definitions
        ordered_player_list=[]
        player_dict_by_pos={}
        for player in self.players:
            if player.position in player_dict_by_pos.keys():
                player_dict_by_pos[player.position].append(player)
            else:
                player_dict_by_pos[player.position]=[player]
        for pos in position_output_order:
            if pos not in player_dict_by_pos.keys():
                for pos_ in flex_definitions[pos]:
                    if len(player_dict_by_pos[pos_])>0:
                        ordered_player_list.append(player_dict_by_pos[pos_].pop(-1))
                        break
            else:
                ordered_player_list.append(player_dict_by_pos[pos].pop(-1))
        self.players = ordered_player_list
