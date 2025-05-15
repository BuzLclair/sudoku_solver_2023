# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 12:17:42 2023

@author: const
"""

import pandas as pd
import numpy as np


WD_PATH = r'C:/Users/const/Desktop/'

SUDOKU_GRID = pd.read_excel(WD_PATH + 's.xlsx', index_col=None, header=None)



def grid_cleaner(grid):
    try:
        grid = grid.iloc[:9,:9]
        grid.index, grid.columns = range(9), range(9)
        return grid
    except:
        print('Error grid to small')

SUDOKU_GRID = grid_cleaner(SUDOKU_GRID)



############ Check 1 (numbers possibles)

class checker_level_1:
    def __init__(self, grid):
        self.grid = grid
        self.basic_check = self.check_empty_cell()
        self.row_check = self.check_in_line()
        self.column_check = self.check_in_columns()
        self.block_check = self.check_in_block()
        self.final_check = self.checking_final()

    def check_empty_cell(self):
        return (self.grid != self.grid)

    def check_in_line(self):
        test_val = np.ones(self.grid.shape)
        test_lines = []
        for nb in range(1,10):
            check_in_line = list(map(lambda x: nb not in list(x[1]), list(SUDOKU_GRID.iterrows())))
            test_lines.append((test_val.T*check_in_line).T)
            test_lines[nb-1] *= self.basic_check
        return test_lines

    def check_in_columns(self):
        test_val = np.ones(self.grid.shape)
        test_col = []
        for nb in range(1,10):
            check_in_col = list(map(lambda x: nb not in list(x[1]), list(SUDOKU_GRID.T.iterrows())))
            test_col.append(test_val*check_in_col)
            test_col[nb-1] *= self.basic_check
        return test_col

    def check_in_block(self):
        test_block = [pd.DataFrame(np.ones(t.shape)) for x in range(9)]
        for row in range(3):
            for col in range(3):
                for nb in range(1,10):
                    test_block[nb-1].iloc[3*row:3*(row+1),3*col:3*(col+1)] *= (nb not in self.grid.iloc[3*row:3*(row+1),3*col:3*(col+1)].values)
        return test_block

    def checking_final(self):
        return list(map(lambda x: self.row_check[x]*self.column_check[x]*self.block_check[x], range(9)))

    def cell_filler(self,grid_to_fill):
        for nb,test_df in enumerate(self.final_check):
            valid_columns = test_df.loc[test_df.sum(axis=0)==1].index
            for col in valid_columns:
                row = test_df.loc[test_df.loc[:,col]==1].index
                grid_to_fill.iloc[row,col] = nb+1

            valid_row = test_df.loc[test_df.sum(axis=1)==1].index
            for row in valid_row:
                col = test_df.loc[test_df.loc[row,:]==1].index
                grid_to_fill.iloc[row,col] = nb+1




############ Check 2 (numbers missing)

class checker_level_2:
    def __init__(self, grid):
        self.grid = grid
        self.basic_check = self.check_empty_cell()
        self.columns_check = self.check_empty_cell_columns()
        self.rows_check = self.check_empty_cell_rows()
        self.blocks_check = self.check_empty_cell_blocks()

    def check_empty_cell(self):
        return (self.grid != self.grid)

    def check_empty_cell_columns(self):
        checker_col = (self.basic_check.sum(axis=0)==1)*self.basic_check
        return 1*checker_col

    def check_empty_cell_rows(self):
        checker_row = (self.basic_check.sum(axis=1)==1)*self.basic_check
        return 1*checker_row

    def check_empty_cell_blocks(self):
        checker_block = pd.DataFrame(np.ones(self.grid.shape))
        for row in range(3):
            for col in range(3):
                checker_block.iloc[3*row:3*(row+1),3*col:3*(col+1)] *= (sum(self.basic_check.iloc[3*row:3*(row+1),3*col:3*(col+1)].sum(axis=0))==1)
        return 1*checker_block*self.basic_check

    def cell_filler(self, grid_to_fill):
        temp_grid = grid_to_fill.loc[:,self.columns_check.sum(axis=0)==1]
        for col in temp_grid.columns:
            nb_to_fill = [nb for nb in range(1,10) if nb not in temp_grid.loc[:,col].values]
            grid_to_fill.loc[:,col].fillna(nb_to_fill[0], inplace=True)

        temp_grid = grid_to_fill.loc[self.rows_check.sum(axis=1)==1,:]
        for row in temp_grid.index:
            nb_to_fill = [nb for nb in range(1,10) if nb not in temp_grid.loc[row,:].values]
            grid_to_fill.loc[row,:].fillna(nb_to_fill[0], inplace=True)



# t1=checker_level_2(SUDOKU_GRID)
# t2=t1.columns_check







############ Check 3 (possibilities enumerating --> bolean)






############ Solving


t=SUDOKU_GRID.copy(deep=True)
t0=pd.DataFrame(np.zeros(SUDOKU_GRID.shape))

while t0.equals(SUDOKU_GRID) != True:
    t0=SUDOKU_GRID.copy(deep=True)
    checker_level_1(SUDOKU_GRID).cell_filler(SUDOKU_GRID)
    # checker_level_2(SUDOKU_GRID).cell_filler(SUDOKU_GRID)
    print('Solve')








