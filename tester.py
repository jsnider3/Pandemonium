import pandemic
import unittest

class Tests(unittest.TestCase):

  def test_neighbors(self):
    ''' Check that everyone has the correct number of neighbors. '''
    brd = pandemic.load_board()
    assert len(brd.neighbors('Hong Kong')) == 6
    assert len(brd.neighbors('Bangkok')) == 5
    assert len(brd.neighbors('Chennai')) == 5
    assert len(brd.neighbors('Kolkata')) == 4
    assert len(brd.neighbors('Delhi')) == 5
    assert len(brd.neighbors('Ho Chi Minh')) == 4
    assert len(brd.neighbors('Manila')) == 5
    assert len(brd.neighbors('Jakarta')) == 4
    assert len(brd.neighbors('Karachi')) == 5
    assert len(brd.neighbors('Baghdad')) == 5
    assert len(brd.neighbors('Taipei')) == 4
    assert len(brd.neighbors('Mumbai')) == 3
    assert len(brd.neighbors('Tehran')) == 4
    assert len(brd.neighbors('Shanghai')) == 5
    assert len(brd.neighbors('Istanbul')) == 6
    assert len(brd.neighbors('Cairo')) == 5
    assert len(brd.neighbors('Sydney')) == 3
    assert len(brd.neighbors('Riyadh')) == 3
    assert len(brd.neighbors('San Francisco')) == 4
    assert len(brd.neighbors('Algiers')) == 4
    assert len(brd.neighbors('Tokyo')) == 4
    assert len(brd.neighbors('Paris')) == 5
    assert len(brd.neighbors('Moscow')) == 3
    assert len(brd.neighbors('Los Angeles')) == 4
    assert len(brd.neighbors('Madrid')) == 5
    assert len(brd.neighbors('Chicago')) == 5
    assert len(brd.neighbors('Milan')) == 3
    assert len(brd.neighbors('Seoul')) == 3
    assert len(brd.neighbors('St. Petersburg')) == 3
    assert len(brd.neighbors('Essen')) == 4
    assert len(brd.neighbors('London')) == 4
    assert len(brd.neighbors('Mexico City')) == 5
    assert len(brd.neighbors('Osaka')) == 2
    assert len(brd.neighbors('Beijing')) == 2
    assert len(brd.neighbors('New York')) == 4
    assert len(brd.neighbors('Khartoum')) == 4
    assert len(brd.neighbors('Bogota')) == 5
    assert len(brd.neighbors('Miami')) == 4
    assert len(brd.neighbors('Washington')) == 4
    assert len(brd.neighbors('Sao Paulo')) == 4
    assert len(brd.neighbors('Montreal')) == 3
    assert len(brd.neighbors('Lima')) == 3
    assert len(brd.neighbors('Lagos')) == 3
    assert len(brd.neighbors('Kinshasa')) == 3
    assert len(brd.neighbors('Buenos Aires')) == 2
    assert len(brd.neighbors('Johannesburg')) == 2
    assert len(brd.neighbors('Santiago')) == 1

  def test_numcities(self):
    ''' Check that we're not missing cities. '''
    brd = pandemic.load_board()
    assert len(brd) == 48

  def test_numlayouts(self):
    ''' Check how many layouts there are with n centers. '''
    brd = pandemic.load_board()
    assert len(list(pandemic.center_placements(brd, 1))) == 1
    assert len(list(pandemic.center_placements(brd, 2))) == 47
    assert len(list(pandemic.center_placements(brd, 3))) == 1081

if __name__ == '__main__':
  unittest.main()
