import networkx as nx

if __name__ == '__main__':
  board = nx.read_edgelist('board.dat', delimiter=',')
  for node in board:
    print board.neighbors(node)


