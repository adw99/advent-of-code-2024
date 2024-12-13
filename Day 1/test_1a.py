from puzzle_1_a import read_data_file, process_data_string, abs_sum

def test_small():
    la = [1,2,3]
    lb = [2,3,4]
    assert(abs_sum(la,lb) == 3)