from puzzle_1_b import read_data_file, process_data_string, total

def test_full_data():
    tx = read_data_file('puzzle-1.txt')
    la, lb = process_data_string(tx)
    assert total(la,lb) == 18805872

def test_small():
    la = [1,2,3]
    lb = [2,3,4]
    assert(total(la,lb) == 5)