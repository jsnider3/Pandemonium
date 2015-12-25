'''
  Code to help me analyze the board game Pandemic.
  @author: Josh Snider
'''

import itertools
import networkx as nx
from scipy import stats

class Board(nx.Graph):

  def __init__(self):
    ''' Subclass a networkx graph.'''
    nx.Graph.__init__(self, self.default_board())
    self.shortest_paths = nx.shortest_path_length(self)

  def best_placements(board, numcenters):
    ''' Get the places you can put n research centers to
        minimize the average distance to a research center. '''
    avg = lambda x: float(sum(x))/len(x)
    best = None
    bestVal = 50
    for placement in board.center_placements(numcenters):
      dists = board.research_dist(placement).values()
      curVal = avg(dists)
      if curVal < bestVal:
        best = [placement]
        bestVal = curVal
      elif curVal == bestVal:
        best.append(placement)
    return best

  def center_placements(board, numcenters):
    ''' Iterate over the possible placements of a given number of
        research centers. '''
    assert  6 >= numcenters >= 1
    cities = set(board)
    cities.remove("Atlanta")
    for combo in itertools.combinations(cities, numcenters - 1):
      yield ["Atlanta"] + list(combo)

  def default_board(self):
    ''' A graph representing the stock board. '''
    return nx.read_edgelist('board.dat', delimiter=',')

  def print_connectivity(board):
    ''' Print some statistics about the nodes' centrality
        and connectivity. '''
    centrality = nx.eigenvector_centrality(board, max_iter=1000)
    ranking = []
    eigens = []
    connections = []
    for node in centrality:
      eigen = centrality[node]
      num_neighbors = len(board.neighbors(node))
      eigens.append(eigen)
      connections.append(num_neighbors)
      ranking.append([node, str(eigen), str(num_neighbors)])
    for line in sorted(ranking, key=lambda x: x[1]):
      print line
    (corr, pvalue) = stats.pearsonr(eigens, connections)
    print('There\'s a very strong correlation between a node\'s degree and ' +
      'centrality. The correlation is ' + str(corr) + ' with a very strong ' +
      'p-value of ' + str(pvalue) + '.')

  def research_dist(board, centers):
    ''' Calculate the distance between each city and the given centers
        and return it as a map. '''
    dists = board.shortest_paths
    retval = {}
    for city in board:
      for center in centers:
        dist = dists[city][center]
        if city not in retval or retval[city] > dist:
          retval[city] = dist
    return retval

if __name__ == '__main__':
  print('First, we load the board from a saved edge list.')
  board = Board()
  print('Then we replicate Matt Wigway\'s results from him blog post at '
    + 'http://www.indicatrix.org/2014/03/26/overanalyzing-board-games-network-analysis-and-pandemic/.')
  board.print_connectivity()
  print('Now what we want is to find a set of n cities, where we can put ' +
    'research centers in order to minimize the average and max distances ' +
    'from a city without to a city with a research center. We are interested ' +
    'in values of n between 1 and 6 (inclusive) as we don\'t have enough ' +
    'pieces to have more than six research centers. An important constraint, ' +
    'is that we are required to have one research center in Atlanta. As per ' +
    'http://math.stackexchange.com/q/1309646/, this is reducible to the ' +
    'problem of finding a dominating set which is known to be NP-Hard. ' +
    'Fortunately, this problem (despite being NP-Complete) is likely to be ' +
    'solvable in reasonable time for a problem as small as ours.')

