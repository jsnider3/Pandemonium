import itertools
import networkx as nx
from scipy import stats

def load_board():
  return nx.read_edgelist('board.dat', delimiter=',')

def print_connectivity(board):
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

def center_placements(board, numcenters):
  ''' Iterate over the possible placements of a given number of
      research centers. '''
  assert  6 >= numcenters >= 1
  cities = set(board)
  cities.remove("Atlanta")
  for combo in itertools.combinations(cities, numcenters - 1):
    yield ["Atlanta"] + list(combo)

if __name__ == '__main__':
  print('First, we load the board from a saved edge list.')
  board = load_board()
  print('Then we replicate Matt Wigway\'s results from him blog post at '
    + 'http://www.indicatrix.org/2014/03/26/overanalyzing-board-games-network-analysis-and-pandemic/.')
  print_connectivity(board)
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

