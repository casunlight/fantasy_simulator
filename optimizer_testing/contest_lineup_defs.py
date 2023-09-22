# Define lineup defs for each site/sport. They dont really change ever, so no need to make overly dynamic

from lineup import Lineup_Rule

def retrieve_definitions(site='DRAFTKINGS', sport='NFL', contest_type='CLASSIC', field='LINEUP_RULE'):
    try:
        return DEFINITIONS[site.upper()][sport.upper()][contest_type.upper()][field.upper()]
    except:
        raise ValueError(f'DEFINITIONS[{site}][{sport}][{contest_type}][{field}] not found!')




#All keys upper case
DEFINITIONS={
    'DRAFTKINGS':{
        'NFL':{
            'CLASSIC':{
                'LINEUP_RULE':Lineup_Rule(position_ordered_list=['QB','RB','RB','WR','WR','WR','TE','FLEX','DST'],
                                   flex_definitions={'FLEX':['RB','TE','WR']},
                                   salary_cap=50000, score_mult=None, salary_mult=None),
                'REQUIRED_COLS': ['position', 'name + id', 'name', 'id', 'roster position', 'salary', 'game info', 'teamabbrev', 'proj', 'ownership', 'opponent']
            },
            'SHOWDOWN':{
                'LINEUP_RULE':Lineup_Rule(position_ordered_list=['CPTN','FLEX','FLEX','FLEX','FLEX','FLEX'],
                                   flex_definitions={},
                                   salary_cap=50000, score_mult={'CPTN': 1.5}, salary_mult={'CPTN': 1.5}),
                'REQUIRED_COLS': ['position', 'name + id', 'name', 'id', 'roster position', 'salary', 'game info', 'teamabbrev', 'proj', 'ownership', 'opponent']
            }
                                
        }    
    },
    'FANDUEL':{
        'NFL':{
            'CLASSIC':{
                'LINEUP_RULE':Lineup_Rule(position_ordered_list=['QB','RB','RB','WR','WR','WR','TE','FLEX','DST'],
                                   flex_definitions={'FLEX':['RB','TE','WR']},
                                   salary_cap=60000, score_mult=None, salary_mult=None),
                'REQUIRED_COLS': ['Player ID + Player Name','Id','Position','Nickname','Salary','Game',	'Team','Opponent']
            },
            'SHOWDOWN':{
                'LINEUP_RULE':Lineup_Rule(position_ordered_list=['CPTN','FLEX','FLEX','FLEX','FLEX','FLEX'],
                                   flex_definitions={},
                                   salary_cap=50000, score_mult={'CPTN': 1.5}, salary_mult=None),
                'REQUIRED_COLS': ['Player ID + Player Name','Id','Position','Nickname','Salary','Game',	'Team','Opponent']
            }
                                
        }    
    },
    
}

