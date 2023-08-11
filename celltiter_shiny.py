#! /home/nberi/miniconda3/bin/python

# need to be able to parse input arguments
import argparse

# need pandas and numpy to do math on data frame 
import pandas as pd
import numpy as np

# initialize the parser
parser = argparse.ArgumentParser()

# name of ctg values file - must be unmodified from ctg computer 
parser.add_argument('filename')

# starting volume - assume 1000 ul default
parser.add_argument('-v1', '--starting_volume', default = '1000')

# this is the conc desired and the value input should be the # ul 
# into which a million rlu should be dissolved
parser.add_argument('-c2', '--final_rlu_conc', default='100')

# arguments as a . . . class??
args = parser.parse_args()

filename = args.filename
starting_volume = int(args.starting_volume)

# define fxn for getting df
def produce_dataframe(fname, starting_vol):
    fraction = starting_vol / 1000
    final_conc = int(args.final_rlu_conc)
    # how much to divide the raw rlu value by
    dividend = 1000000 / final_conc

    # Name of input file 
    title = str(fname)
#    print(title)

    # open your ctg file of interest 
    with open(fname, encoding = 'utf8', errors = 'ignore') as in_file:
       file_lines = [line.rstrip().split('\t') for line in in_file]
       # make a list of just the lines with data, ie those in the 96-well plate
       lines = file_lines[4:12]
       
    # if there are blank columns at the right there will be fewer than 12 columns in the output table
    # add 12 - n columns here

    for line in lines:
        num_cols = len(line)
        num_cols_to_add = 14 - num_cols
    #    print('Add', num_cols_to_add, 'columns to the existing', num_cols, 'columns.')
        for i in range(num_cols_to_add):
            line.append(0)
         
    # create df
    # change rlu values to int that is divided by 1e4 and rounded to nearest ten 
    df = pd.DataFrame(lines).drop([0,1], axis='columns').apply(pd.to_numeric).fillna(0).div(dividend).multiply(fraction).round(-1).astype('Int64')

    # # # label rows and columns in agreement with 96-well plate naming scheme
    # df.index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    # df.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    df = df.to_string(header = False, index = False)

    # return the labeled dataframe
    return df
    
g = produce_dataframe(filename, starting_volume)

print(g)