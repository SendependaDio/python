import random
from timeit import default_timer as timer
d = {1: 'A',
     2: 'B',
     3: 'C',
     4: 'D',
     5: 'E'
     }

d_prc = {}


def file_write(file_name, str):
    with open(file_name, 'w') as out:
        out.write(str)


def dict_output(d):
    for key in d:
        print(key, ':', sep='', end=' ')
        print(d[key], end='%')
        print()


def update_dictionary(d, key, value, mode='list'):
    if mode == 'list_up':
        if key in d:
            d[key] += value
        else:
            d[key] = 0
            d[key] += value


def cnt_prc(str, number, dict):
    for i in range(len(str)):
        if i % 2 == 0:
            update_dictionary(dict, str[i], 1, 'list_up')
    for key in dict:
        dict[key] = dict[key] / number * 100


def main():
    number = int(input())
    my_str = ''
    start = timer()
    for i in range(number):
        k = random.randint(1, 5)
        my_str += d[k]
        my_str += ' '

    print(my_str)
    file_write('output.txt', my_str)
    cnt_prc(my_str, number, d_prc)
    dict_output(d_prc)
    duration = timer() - start
    print('Time:', duration)


main()
