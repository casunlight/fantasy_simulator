

import numpy as np
import pandas as pd
import time
from itertools import repeat


#SOME DEFAULT VALUES FOR OUR MODULE
#For an average golfer(datagolf index=0, or field average)
par3_score_to_par_defaults = np.array([-2,-1,0,1,2])
par3_score_to_par_proba_defaults = np.array([.003, 0.15, 0.7, 0.1, 0.047])

par4_score_to_par_defaults = np.array([-2,-1,0,1,2])
par4_score_to_par_proba_defaults = np.array([.003, 0.15, 0.7, 0.1, 0.047])

par5_score_to_par_defaults = np.array([-2,-1,0,1,2])
par5_score_to_par_proba_defaults = np.array([.02, 0.15, 0.7, 0.1, 0.03])


class Hole():
    """Initialize a hole object, with its various probabilities for different scores relative to par"""
    def __init__(self, par=4, score_to_par=par4_score_to_par_defaults, score_to_par_proba=par4_score_to_par_proba_defaults):

        #Object type-checking
        #Throw an exception if score_to_par or score_to_par_proba arent a list or an ndarray, convert to ndarry if a list
        if not(isinstance(score_to_par,list)) and not(isinstance(score_to_par,np.ndarray)):
            raise ValueError('score_to_par and score_to_par_proba need to be of type list or np.ndarray')
        
        if not(isinstance(score_to_par,np.ndarray)):
            score_to_par = np.array(score_to_par)

        if not(isinstance(score_to_par_proba,np.ndarray)):
            score_to_par_proba = np.array(score_to_par_proba)

        #Begin creating our hole objects attributes
        if par==3:
            self.par=3
            if np.array_equiv(score_to_par,par4_score_to_par_defaults):
                self.score_to_par=par3_score_to_par_defaults
            else:
                self.score_to_par=score_to_par
            if np.array_equiv(score_to_par_proba,par4_score_to_par_proba_defaults):
                self.score_to_par_proba=par3_score_to_par_proba_defaults
            else:
                self.score_to_par_proba=score_to_par_proba
        elif par==5:
            self.par=5
            if np.array_equiv(score_to_par,par4_score_to_par_defaults):
                self.score_to_par=par5_score_to_par_defaults
            else:
                self.score_to_par=score_to_par
            if np.array_equiv(score_to_par_proba,par4_score_to_par_proba_defaults):
                self.score_to_par_proba=par5_score_to_par_proba_defaults
            else:
                self.score_to_par_proba=score_to_par_proba 
        else:
            self.par=par
            self.score_to_par=score_to_par
            self.score_to_par_proba=score_to_par_proba

        


        #if the arrays score_to_par and score_to_par_proba dont have same length, throw exception
        if len(self.score_to_par) != len(self.score_to_par_proba):
            raise ValueError('Length of score array does not equal length of score proba array!')
 
        
        #If score_to_par is missing 0 (par), append it
        if 0 not in self.score_to_par:
            print('par not in inputted score_to_par array, adding it and assigning probability to sum to 1')
            self.score_to_par = np.append(self.score_to_par,0)
            current_proba = sum(self.score_to_par_proba)
            self.score_to_par_proba = np.append(self.score_to_par_proba,1-current_proba)

        
        #If probabilities don't sum to 1, alert the user that remaining probability will be assigned to par
        if sum(self.score_to_par_proba)!=1:
            #print('hole score proba does not sum to 1, remaining proba added to par')
            proba_diff = 1 - sum(self.score_to_par_proba)
            for i in range(len(self.score_to_par)):
                if self.score_to_par[i]==0:
                    self.score_to_par_proba[i] = self.score_to_par_proba[i] + proba_diff
        


    def return_score_to_par_proba(self, expected_sg=0.0, gamma=0.0):
        return np.array(self.score_to_par_proba)
    
    def return_score_to_par(self, expected_sg=0.0, gamma=0.0):
        return np.array(self.score_to_par)
    
    def return_scoring_avg(self, expected_sg=0.0, gamma=0.0):
        return sum(self.score_to_par_proba*self.score_to_par)+self.par
    
    def simulate_score_to_par(self, num=1, expected_sg=0.0, gamma=0.0):
        ele = self.score_to_par.tolist()
        #print('ele: '+ str(ele))
        proba = self.score_to_par_proba.tolist()
        #print('proba' + str(proba))
        return np.random.choice(a=ele, size=num, replace=True, p=proba)#For larger sims   can do it all at once for one player/hole
    
    def simulate_score(self, num=1, expected_sg=0.0, gamma=0.0):
        ele = (self.par + self.score_to_par).tolist()
        proba = self.score_to_par_proba.tolist()
        #np.random.choice(elements, 10, p=probabilities)
        return np.random.choice(a=ele, size=num, replace=True, p=proba)#For larger sims   can do it all at once for one player/hole
    
    def norm_scoring_avg_to_par(self):
        """If supplied score probabilities yield an expectation different than par, this function will normalize the probabilities
        of either the over par scores, or the under par scores (keeping their relative probabilities even) such that the 
        #expected score is exactly equal to par. Basically a function of convenience."""

        cond_exp_under_par = 0
        cond_exp_over_par = 0

        for i in range(len(self.score_to_par)):
            if self.score_to_par[i] < 0:
                cond_exp_under_par+=self.score_to_par[i]*self.score_to_par_proba[i]
            elif self.score_to_par[i] > 0:
                cond_exp_over_par+=self.score_to_par[i]*self.score_to_par_proba[i]


        for i in range(len(self.score_to_par)):
            if self.score_to_par[i] < 0:
                if abs(cond_exp_under_par)>abs(cond_exp_over_par):
                    self.score_to_par_proba[i] = self.score_to_par_proba[i]*abs(cond_exp_over_par/cond_exp_under_par) 
            elif self.score_to_par[i] > 0:
                if abs(cond_exp_under_par)<abs(cond_exp_over_par):
                    self.score_to_par_proba[i] = self.score_to_par_proba[i]*abs(cond_exp_under_par/cond_exp_over_par) 


        new_total_proba = sum(self.score_to_par_proba)
        #print('new_total_proba: '+str(new_total_proba))

        #insert probability removed from under/over par scoring and insert into par
        for i in range(len(self.score_to_par)):
            if self.score_to_par[i] == 0:
                self.score_to_par_proba[i] = self.score_to_par_proba[i] + (1-new_total_proba)


    def norm_scoring_avg_to_x_vs_exp(self, sg=0, inplace=True):
        """If supplied score probabilities yield an expectation different than sg=x, this function will normalize the probabilities
        of the over par scores and the under par scores (current model is 50% expectation comes from over/underpar) such that the 
        #expected score is exactly equal to current expected score - sg=x. Basically a function of convenience. For example if
        the scoring avg is 4.05 for an sg=0 player and we are asked to normalize probabilities for an sg=.15, the function will
        normalize the probabilities of the hole such that the expected score is 3.9"""

        #Think of _sg0 denoting the expectation for a strokes gained=0 player
        sum_exp_under_par_sg0 = 0
        sum_prob_under_par_sg0 = 0
        sum_exp_over_par_sg0 = 0
        sum_prob_over_par_sg0 = 0

        for i in range(len(self.score_to_par)):
            if self.score_to_par[i] < 0:
                sum_exp_under_par_sg0+=self.score_to_par[i]*self.score_to_par_proba[i]
                sum_prob_under_par_sg0+=self.score_to_par_proba[i]
            elif self.score_to_par[i] > 0:
                sum_exp_over_par_sg0+=self.score_to_par[i]*self.score_to_par_proba[i]
                sum_prob_over_par_sg0+=self.score_to_par_proba[i]

        #print('sum_exp_over_par_sg0: ' + str(sum_exp_over_par_sg0))
        #print('sum_exp_under_par_sg0: ' + str(sum_exp_under_par_sg0))
        #print('sum_prob_over_par_sg0: ' + str(sum_prob_over_par_sg0))
        #print('sum_prob_under_par_sg0: ' + str(sum_prob_under_par_sg0))

        #Here, we calculate the expected score of a player who is expected to gain sg=x on this hole
        player_exp_score_sgx = self.return_scoring_avg() - sg
        #print('player_exp_score_sgx: ' + str(player_exp_score_sgx))

        #This is a MODEL for how the delta of expectation changes for under par and over par scenarios
        #It probably should NOT be linear for all types of holes, but for players close to par .. it should be close to even
        #between over par and under par scenarios .. I.e. his edge comes evenly from both making fewer bogeys and making more birdies
        over_par_delta_constant = .5
        under_par_delta_constant = .5

        #How much expectation is needed from making over/under par scenarios to get the players expected sg where it needs to be
        exp_needed_over_par_sgx=sg*over_par_delta_constant
        exp_needed_under_par_sgx=sg*under_par_delta_constant
        #print('exp_needed_over_par_sgx: ' + str(exp_needed_over_par_sgx))
        #print('exp_needed_under_par_sgx: ' + str(exp_needed_under_par_sgx))

        #Expectation was originally defined in terms of score vs. par, so subtract expectation for sg > 0
        new_exp_over_par_sgx = sum_exp_over_par_sg0 - exp_needed_over_par_sgx
        new_exp_under_par_sgx = sum_exp_under_par_sg0 - exp_needed_under_par_sgx
        #print('new_exp_over_par_sgx: ' + str(new_exp_over_par_sgx))
        #print('new_exp_under_par_sgx: ' + str(new_exp_under_par_sgx))

        #To get the new probabilities needed over and under par, simply scale the old probability by the ratio of old expectation for sg0 and new expectation for sgx
        #I.e. we are keeping relative rates of bogey/double birdie/eagle constant
        new_prob_over_par_sgx = (new_exp_over_par_sgx/sum_exp_over_par_sg0)*sum_prob_over_par_sg0
        new_prob_under_par_sgx = (new_exp_under_par_sgx/sum_exp_under_par_sg0)*sum_prob_under_par_sg0
        #print('new_prob_over_par_sgx: ' + str(new_prob_over_par_sgx))
        #print('new_prob_under_par_sgx: ' + str(new_prob_under_par_sgx))

        new_prob_list_sgx=[]
        prob=0

        #Scale the old over/under par probabilities based on what we solved for that we needed before
        for i in range(len(self.score_to_par_proba)):
            if self.score_to_par[i] < 0:
                prob=self.score_to_par_proba[i]*new_prob_under_par_sgx/sum_prob_under_par_sg0
            elif self.score_to_par[i] > 0:
                prob=self.score_to_par_proba[i]*new_prob_over_par_sgx/sum_prob_over_par_sg0
            else:
                prob = self.score_to_par_proba[i]
            new_prob_list_sgx.append(prob)
        #print('new_prob_list_sgx: ' + str(new_prob_list_sgx))
        #print('sum new_prob_list: ' + str(sum(new_prob_list_sgx)))

        #Scale the probability of par such that total probability sums to 1 (in this model p(par) will always decrease slightly, is this good?)
        for i in range(len(self.score_to_par_proba)):
            if self.score_to_par[i] == 0:
                new_prob_list_sgx[i] = new_prob_list_sgx[i] + (1 - sum(new_prob_list_sgx))
        #print('new_prob_list_sgx: ' + str(new_prob_list_sgx))
        #print('sum new_prob_list_sgx: ' + str(sum(new_prob_list_sgx)))

        
        #If inplace==True, return a new hole object, else reset the hole objects score_to_par_proba such that expectation changes to our liking
        if inplace==True:
            self.score_to_par_proba = np.array(new_prob_list_sgx)
        else:
            return Hole(par=self.par, score_to_par=self.score_to_par, score_to_par_proba=np.array(new_prob_list_sgx))
        






class Player():
    def __init__(self, name='none given', sg_true = 0, sg_vol=2):
        self.name=name
        self.sg_true = sg_true
        self.sg_vol = sg_vol
        

    def simulate_hole(self, hole, n=1, sg_ovrd=None):
        """Return an array of scores for given hole"""

        #Consider changing this for par 3s, 4s, 5s, as good players usually gain more on par5s
        if sg_ovrd==None:
            hole_sg = self.index/18
        else:
            hole_sg = sg_ovrd

        #Change the proba for the hole to account for the particular player
        adj_hole = hole.norm_scoring_avg_to_x_vs_exp(sg=hole_sg, inplace=False)

        return adj_hole.simulate_score(num=n)


    def simulate_round(self, course, n=1, sg_ovrd=None):
        """Return an array of scores given a course. Both a round score but also each individual hole"""

        #The map() function in Python provides an efficient way to apply a function to each element in a list. 
        #It takes two arguments: the function to be applied and the iterable (list) on which the function will be applied. 
        #The map() function returns a map object, which can be converted to a list using the list() function.



        scores = list(map(self.simulate_hole, course.holes, repeat(n)))
        #https://stackoverflow.com/questions/10834960/how-to-do-multiple-arguments-to-map-function-where-one-remains-the-same
        #The docs explicitly suggest this is the main use for itertools.repeat:
        #Make an iterator that returns object over and over again. Runs indefinitely unless the times argument is specified. 
        #Used as argument to map() for invariant parameters to the called function. 
        #Also used with zip() to create an invariant part of a tuple record.
        
        #list(map(pow, range(10), repeat(2)))

        return scores
    
\

        





default_holes = [Hole(par=4),Hole(par=4),Hole(par=4),Hole(par=4),Hole(par=3),Hole(par=5),Hole(par=3),Hole(par=5),Hole(par=4), \
                Hole(par=4),Hole(par=4),Hole(par=4),Hole(par=4),Hole(par=3),Hole(par=5),Hole(par=3),Hole(par=5),Hole(par=4)]


class Course():
    def __init__(self, name='none given', holes=default_holes):
        self.name=name
        self.holes=holes
        par=0
        for hole in holes:
            par+=hole.par
        self.par=par
        expected_score=0
        for hole in holes:
            expected_score+=hole.return_scoring_avg()
        self.expected_score=expected_score


class Tourney():
    def __init__(self, player_list, course, name='none given'):
        self.player_list=player_list
        self.course = course
        self.name = name













    