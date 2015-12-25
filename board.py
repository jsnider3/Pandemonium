import networkx as nx

def load_board():
  return nx.read_edgelist('board.dat', delimiter=',')

if __name__ == '__main__':
  board = load_board()
  centrality = nx.eigenvector_centrality(board, max_iter=1000)
  stuff = []
  for node in centrality:
    stuff.append([node, str(centrality[node]), str(len(board.neighbors(node)))])
  for line in sorted(stuff, key=lambda x: x[1]):
    print line


