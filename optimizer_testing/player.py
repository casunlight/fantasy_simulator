## Define objects related to individual players
import numpy as np


class Slate_Player():
    def __init__(self, name, slate_name_id, position, var_name, game_time, base_proj, percent_own, stdev):
        self.name=name
        self.slate_name_id = slate_name_id
        self.position = position
        self.var_name = var_name
        self.game_time = game_time
        self.base_proj = base_proj
        self.percent_own = percent_own
        self.stdev=stdev
        self._sim_score=0

    def __str__(self):
        return self.slate_name_id
    
    def __repr__(self):
        return self.slate_name_id
    
    def __eq__(self, other):
        if isinstance(other, Slate_Player):
            return self.slate_name_id==other.slate_name_id
        return False
    
    def simulate_score(self):
        #This method will not invoke correlation since only one player is in scope
        return np.random.normal(self.base_proj, self.stdev)