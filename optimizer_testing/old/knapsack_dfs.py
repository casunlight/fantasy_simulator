import time
import pandas as pd
import numpy as np

def solve_knapsack(projections, salaries, max_budget, poss_budgets):
  # create a two dimensional array for Memoization, each element is initialized to '-1'
  
  dp = [[-1 for y in poss_budgets] for x in range(len(projections))]#List (of #num_player length) of lists (size possible_lineup_salaries)
  print('type dp: '+ str(type(dp)))
  print('shape dp: '+ str(np.shape(dp)))
  #print('dp: '+str(dp))
  return knapsack_recursive(dp, projections, salaries, max_budget, poss_budgets, 0)


def knapsack_recursive(dp, projections, salaries, budget, poss_budgets, currentIndex):

  # base case checks
  if budget <= 0 or currentIndex >= len(projections):
    return 0

  # if we have already solved a similar problem, return the result from memory
  if dp[currentIndex][poss_budgets.index(budget)] != -1:
    return dp[currentIndex][poss_budgets.index(budget)]

  # recursive call after choosing the element at the currentIndex
  # if the weight of the element at currentIndex exceeds the capacity, we
  # shouldn't process this
  profit1 = 0
  if salaries[currentIndex] <= budget:
    profit1 = projections[currentIndex] + knapsack_recursive(
      dp, projections, salaries, budget - salaries[currentIndex], poss_budgets, currentIndex + 1)

  # recursive call after excluding the element at the currentIndex
  profit2 = knapsack_recursive(
    dp, projections, salaries, budget, poss_budgets, currentIndex + 1)

  dp[currentIndex][poss_budgets.index(budget)] = max(profit1, profit2)

  return dp[currentIndex][poss_budgets.index(budget)]





def main():
  
  N=825#First N players
  salary_step=100
  max_budget = 50000
  poss_budgets=range(0,max_budget+salary_step,salary_step)#Need to factor in all budgets 100 .. 50000 else the recursion wont work

  df = pd.read_csv('Week1_Proj.csv')
  print('len df: '+str(df.shape[0]))#825 rows
  projections = df['Proj'].tolist()[:N]
  salaries = df['Salary'].tolist()[:N]
  print('len salaries: '+str(len(salaries)))
  
  tic = time.perf_counter()
  print('soln: '+str(solve_knapsack(projections, salaries, max_budget, poss_budgets)))
  toc = time.perf_counter()
  print('time elapsed: '+str(toc-tic))





main()

