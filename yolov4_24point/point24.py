# _*_coding:utf-8_*_

#**************head**********************#
#author: Liu Minglai
#reference from github:
#https://github.com/MiracleYoung/You-are-Pythonista/tree/master/PythonExercise/App/python_24/xujin
#
#change history:
#v01: 6/9/2020 10:58:59: extend to 13(J,Q,K),delete bracket calculation
#v02: 6/9/2020 4:23:26 : add auto generate 4 number function.
#v03: 6/9/2020 5:55:51 : auto loop for training, add pause to exit or wait for answer
#v04: 6/10/2020 10:10  : recover bracket calculation
#v05: 6/10/2020 2:57   : input number version, fix answer showing bug(some effective answer is missing)
#v06: 6/10/2020 3:20   : recover auto gen
#v61: 11/21/2020 19:40 : based on v6, adapt with poker detect program
#v07: 12/06/2020 10:40 : clean the comments and code
#*****************************************#

from collections.abc import Iterable
from itertools import product,permutations,zip_longest,chain
import math
import random
import msvcrt

import os

class Point24():
    # define the operation array
    OPERATIONS = ('+','-','*','/')

    # define the string format
    FORM_STRS = [
        # one bracket case
        '( %s %s %s ) %s %s %s %s',
        '( %s %s %s %s %s ) %s %s',
        '( %s %s %s %s %s %s %s )',
        '%s %s ( %s %s %s ) %s %s',
        '%s %s ( %s %s %s %s %s )',
        '%s %s %s %s ( %s %s %s )',
        # two bracket case
        '( %s %s %s ) %s ( %s %s %s )',
        '( ( %s %s %s ) %s %s ) %s %s',
        '( %s %s ( %s %s %s ) ) %s %s',
        '%s %s ( ( %s %s %s ) %s %s )',
        '%s %s ( %s %s ( %s %s %s ) )',

        # three bracket case is duplicated, No need
    ]

    def __init__(self,data_iter):
        # judge the input object is Iterable
        #if not isinstance(data_iter, Iterable):
        #    raise TypeError(f'{data_iter} cat`t iter')

        self.data_iter = data_iter

    def _get_all_operation_sequence(self):
        '''
        from self.OPERATIONS to choose one word, generator one array
        return generator
        :return:
        '''
        return product(self.OPERATIONS,repeat=3)

    def _get_all_data_sequence(self):
        '''
        for the input data, generator all sequence
        :return:
        '''
        return permutations(self.data_iter)

    def _format_str(self,calculate_str):
        # format the input data to strings with bracket
        for format_str in self.FORM_STRS:
            yield format_str % (
                calculate_str[0],
                calculate_str[1],
                calculate_str[2],
                calculate_str[3],
                calculate_str[4],
                calculate_str[5],
                calculate_str[6]
            )

    def _hex2int_str(self,calculate_str):
        # Transform HEX to Dec string
        str_split = calculate_str.split()
        calculate_str_int = []
        #print(str_split)

        for item in str_split:
            if item == 'A':
                calculate_str_int.append('10')
            elif item == 'B':
                calculate_str_int.append('11')
            elif item == 'C':
                calculate_str_int.append('12')
            elif item == 'D':
                calculate_str_int.append('13')
            else: #normal number,opertion and ()
                calculate_str_int.append(item)

        #print(calculate_str_int)
        str_int = ''.join(calculate_str_int)
        #print(str_int)
        return str_int

    def calculate(self):
        '''
        calcuate, resturn the formul
        :return:
        '''
        found = 0

        # check all possible data
        for data_sequence in self._get_all_data_sequence():
            # You get all the operators.
            operation_sequences = self._get_all_operation_sequence()
            # Iterate over all the operators
            for operation_sequence in operation_sequences:
                # Use zip Longest to combine numbers and operators
                value = zip_longest(data_sequence, operation_sequence, fillvalue='')
                value_chain = chain.from_iterable(value)
                calculate_str = ''
                # Iterate over each character and get an expression without parentheses
                for _ in value_chain:
                    calculate_str += _

                #print(calculate_str)

                for finally_calculate_str in self._format_str(calculate_str):
                    try:    # Use the eval function to execute the expression
                        result = eval(self._hex2int_str(finally_calculate_str))
                    except ZeroDivisionError:    # Catch an exception with a dividend of 0, and then skip the loop
                        continue

                    if math.isclose(result, 24):
                        #return calculate_str, result
                        print(self._hex2int_str(finally_calculate_str))
                        found = 1;

        # Run to this location, indicating that you do not find an expression that can calculate 24, and return none
        if found == 0:
            return 'Sorry, NO result'
        else:
            #return calculate_str, result
            return 'Great, Got 24 point see above!'

if __name__ == '__main__':

    #input_str = input('Now start counting the 24 games, please enter the number (1-13), each number is seperated by , :')

    #data_list = input_str.split(',')

    while True:
        data_list_num = random.sample(("123456789ABCD"),4) # value 1-13
        #print(data_list_num)

        data_list_show = []

        for data in data_list_num:
            #print(data)
            if data == '1':
                data_list_show.append('A')
            elif data == 'A':
                data_list_show.append('10')
            elif data == 'B':
                data_list_show.append('J')
            elif data == 'C':
                data_list_show.append('Q')
            elif data == 'D':
                data_list_show.append('K')
            else: #range 2-9, normal number
                data_list_show.append(str(data))

        print('the cards are follow:')
        print(data_list_show)

        input_str = input('Now calculate the 24-point game, press Enter to see the answer, press D to exit')

        if input_str == 'd': #exit if press D
            print('Thanks for using the 24-point training program, practice it well, bye!')
            break

        data_list = list(map(str,data_list_num))  #convert to string type

        print(Point24(data_list).calculate())
        print('\n')
