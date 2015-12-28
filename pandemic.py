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

  def print_best_placements(self):
    print('Now what we want is to find a set of n cities, where we can put ' +
      'research centers in order to minimize the average and max distances ' +
      'from a city without to a city with a research center. We are interested ' +
      'in values of n between 1 and 6 (inclusive) as we don\'t have enough ' +
      'pieces to have more than six research centers. An important constraint, ' +
      'is that we are required to have one research center in Atlanta. As per ' +
      'http://math.stackexchange.com/q/1309646/, this is reducible to the ' +
      'problem of finding a dominating set which is known to be NP-Hard. ' +
      'Fortunately, this problem (despite being NP-Complete) is ' +
      'solvable in reasonable time for a problem as small as ours. ' +
      'Especially when you cache the all-pairs shortest paths matrix.')
    bests = []
    bests.append(self.best_placements(1))
    bests.append(self.best_placements(2))
    bests.append(self.best_placements(3))
    bests.append(self.best_placements(4))
    bests.append(self.best_placements(5))
    bests.append(self.best_placements(6))
    print('Obviously, with only one research center the only possible ' +
      'placement is {0} which is therefore optimal.'.format(str(bests[0])))
    print('With two research centers the optimal solution is to pair Atlanta ' +
      'with either Baghdad or Cairo.')
    print('With three research centers there\'s one optimal solution ' +
      'with the mandatory Atlanta, Hong Kong covering East Asia, and ' +
      'Cairo providing fast travel to Africa, Europe, and the Mideast.')
    print('With four research centers, we take the optimal solution for ' +
      'three, move our Mideast center to Istanbul and put our fourth in ' +
      'Sao Paulo to cover the southwest side of the globe.')
    print('With five research centers, we have a lot of possible choices ' +
      str(bests[4]))
    print('Finally, with six research centers we can cover all corners of ' +
      'the globe with {0}.'.format(', '.join(bests[5][0])))
    print("Of course, it's not possible for us to build a research center " +
      "in Cairo and then move it to Istanbul when that's better for us. "
      "In fact, unless one of the player's is the operations expert it's " +
      "unlikely we can build research stations in the optimal locations " +
      "at will. What we want now is a ranking of which cities are the best " +
      "for research centers and a separation of them into regions where we " +
      "understand that it's never a good deal to put two research centers " +
      "in the same region.")
    self.print_most_often_optimal(bests)
    self.print_regions(bests[-1][0])

  def print_most_often_optimal(self, bests):
    ''' Print those cities which are most often in optimal layouts. '''
    print("The centrality measure previously discussed is a good judge of " +
      "how good building a research center in a city is, but let's check our " +
      "work by counting how many times each city appears in the optimal " +
      "placements.")
    occurences = [item for sublist in bests for subsublist in
      sublist for item in subsublist]
    cities = list(self)
    for city in sorted(cities, key=occurences.count):
      if occurences.count(city):
        print(city, occurences.count(city))

  def print_regions(self, centers):
    ''' Print the voronoi regions for a given list of centers. '''
    print("One way we can separate the world into regions is with a Voronoi " +
      "diagram where each research center in the optimal six center layout " +
      "is the center of a zone.")
    voronoi = self.voronoi_regions(centers)
    for region in voronoi:
      print(region +": " + ', '.join(voronoi[region]))

  def voronoi_regions(self, centers):
    ''' Given a set of center nodes, split the cities up based on which
      center they are closer to. Cities equidistant from two centers
      are split arbitrarily.'''
    retval = {}
    for center in centers:
      retval[center] = []
    for city in self:
      closest = None
      dist = 50
      for center in centers:
        if self.shortest_paths[center][city] < dist:
          closest = center
          dist = self.shortest_paths[center][city]
      retval[closest].append(city)
    return retval

if __name__ == '__main__':
  print('First, we load the board from a saved edge list.')
  board = Board()
  print('Then we replicate Matt Wigway\'s results from him blog post at '
    + 'http://www.indicatrix.org/2014/03/26/overanalyzing-board-games-network-analysis-and-pandemic/.')
  board.print_connectivity()
  board.print_best_placements()

