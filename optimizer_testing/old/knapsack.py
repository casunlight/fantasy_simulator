import time
import pandas as pd
import numpy as np

def solve_knapsack(profits, weights, capacity):
  # create a two dimensional array for Memoization, each element is initialized to '-1'
  dp = [[-1 for x in range(capacity+1)] for y in range(len(profits))]
  print('type dp: '+ str(type(dp)))
  print('shape dp: '+str(np.shape(dp)))
  #print('dp: '+str(dp))
  return knapsack_recursive(dp, profits, weights, capacity, 0)


def knapsack_recursive(dp, profits, weights, capacity, currentIndex):

  # base case checks
  if capacity <= 0 or currentIndex >= len(profits):
    return 0

  # if we have already solved a similar problem, return the result from memory
  if dp[currentIndex][capacity] != -1:
    return dp[currentIndex][capacity]

  # recursive call after choosing the element at the currentIndex
  # if the weight of the element at currentIndex exceeds the capacity, we
  # shouldn't process this
  profit1 = 0
  if weights[currentIndex] <= capacity:
    profit1 = profits[currentIndex] + knapsack_recursive(
      dp, profits, weights, capacity - weights[currentIndex], currentIndex + 1)

  # recursive call after excluding the element at the currentIndex
  profit2 = knapsack_recursive(
    dp, profits, weights, capacity, currentIndex + 1)

  dp[currentIndex][capacity] = max(profit1, profit2)
  return dp[currentIndex][capacity]





def main():
  #values = [1, 6, 10, 16, 5, 6, 1, 1, 1, 1]
  #weights = [1, 2, 3, 5, 2, 1, 1, 1, 1, 1]
  #capacity = 12
  N=50
  df = pd.read_csv('Week1_Proj.csv')
  print('shape df: '+str(df.shape[0]))
  values = df['Proj'].tolist()
  values = values[:N]
  weights = df['Salary'].tolist()
  weights = weights[:N]
  print('len weights: '+str(len(weights)))
  capacity = 50000
  print('soln: '+str(solve_knapsack(values, weights, capacity)))






tic = time.perf_counter()
main()
toc = time.perf_counter()
print('time elapsed: '+str(toc-tic))