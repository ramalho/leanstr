import sys
import time

sys.path.insert(0, '../')

from leanstr import LeanStr

ascii_text = 'War_and_Peace-ASCII.txt'
same_with_ant = 'War_and_Peace-ASCII-with-ant.txt'  

@profile
def load_ascii():
    with open(ascii_text) as fp:
        py_str = fp.read()
    with open(ascii_text, 'rb') as fp:
        my_str = LeanStr(data=fp.read())
    return py_str, my_str

@profile
def load_with_ant():
    with open(same_with_ant) as fp:
        py_str = fp.read()
    with open(same_with_ant, 'rb') as fp:
        my_str = LeanStr(data=fp.read())
    return py_str, my_str

def clock(label, py_str, my_str):
    print(label)
    t0 = time.perf_counter()
    n = len(py_str)
    print('len(py_str) =', n)
    t1 = time.perf_counter()
    print(f'         dt = {t1 - t0:0.5f}s')

    t0 = time.perf_counter()
    n = len(my_str)
    print('len(my_str) =', n)
    t1 = time.perf_counter()
    print(f'         dt = {t1 - t0:0.5f}s')

    print()
    
if __name__ == '__main__':
    a, b = load_ascii()
    clock('ASCII', a, b)
    a, b = load_with_ant()
    clock('ASCII with ant', a, b)
