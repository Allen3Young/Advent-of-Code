#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 14:02:52 2023

@author: yuxuan
"""
import re
import numpy

def is_valid_position(row, col, rows, cols):
    return 0 <= row < rows and 0 <= col < cols

def get_adjacent_numbers(grid, row, col):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    adjacent_numbers = []
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if is_valid_position(new_row, new_col, len(grid), len(grid[0])) and grid[new_row][new_col].isdigit():
            adjacent_numbers.append(int(grid[new_row][new_col]))

    return adjacent_numbers

def sum_of_part_numbers(engine_schematic):
    total_sum = 0

    for i in range(len(engine_schematic)):
        for j in range(len(engine_schematic[0])):
            if engine_schematic[i][j].isdigit():
                adjacent_numbers = get_adjacent_numbers(engine_schematic, i, j)
                total_sum += int(engine_schematic[i][j]) if adjacent_numbers else 0

    return total_sum

def find_numbers_with_indices(input_string):
    pattern = r'\b\d+\b'
    pattern = r'\d+'
    matches = re.finditer(pattern, input_string)
    numbers_with_indices = [(int(match.group()), match.start(), match.end()) for match in matches]

    return numbers_with_indices

def find_star_with_indices(input_string):    
    pattern = r'\*'
    matches = re.finditer(pattern, input_string)
    star_with_indices = [(match.group(), match.start(), match.end() - 1) for match in matches]    
    return star_with_indices
    
def is_symbol(char):
    return not (char.isdigit() or char=='.')

def contain_symbol(string):
    for char in string:
        if is_symbol(char):
            return True
    else:
        return False
    
def is_valid_cur(indices, line):
    res_left = False
    res_right = False
    left_ind, right_ind = indices
    if left_ind > 0:
        res_left = is_symbol(line[left_ind-1])
        print('left', line[left_ind-1])
    if right_ind < len(line):
        res_right = is_symbol(line[right_ind])
        print('right', line[right_ind])
        
    print(line, indices)
    print(res_left, res_right)
    return res_left or res_right

def is_valid_neighbor(indices, line):
    left_ind, right_ind = indices    
    if left_ind > 0:
        left_ind = left_ind - 1    
    if right_ind < len(line): 
        right_ind = right_ind + 1
    print(line[left_ind: right_ind+1])
    return contain_symbol(line[left_ind: right_ind])

def is_contian_star(star_ind, left_ind, right_ind):
    if left_ind <= star_ind +1 and right_ind >= star_ind:
        return True
    return False

# Example engine schematic
engine_schematic = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598.."
]

file_path = '3_input.txt'
with open(file_path, 'r') as file:
    content_list = file.readlines()
        
engine_schematic = content_list
content_list = [line.strip() for line in engine_schematic]
engine_schematic = content_list

n_row = len(engine_schematic)
adjacent_numbers = []
found_numbers_list = []
for i in range(n_row):
    found_numbers = find_numbers_with_indices(engine_schematic[i])
    found_numbers_list.append(found_numbers)
    for i_found_number in found_numbers:
        res_prev = False
        res_post = False
        number, indices = i_found_number[0], i_found_number[1:]
        res_cur = is_valid_cur(indices, engine_schematic[i])        
        if i > 1:
            print("previous line")
            res_prev = is_valid_neighbor(indices, engine_schematic[i-1])
        if i < n_row -1:
            print("next line")
            res_post = is_valid_neighbor(indices, engine_schematic[i+1])
        
        print(number, res_cur, res_prev, res_post)
        if res_cur or res_prev or res_post:
            adjacent_numbers.append(number)
        
sum_numbers = sum(adjacent_numbers)
# find *

new_sum_numbers = 0
for i in range(n_row):
    star = find_star_with_indices(engine_schematic[i])
    print(star)
    if len(star) == 0:
        continue
    for i_star in star:
        print('new star')
        left_ind, right_ind = i_star[1:]
        if left_ind != right_ind:
            pass
        star_ind = left_ind
        
        numbers = found_numbers_list[i]    
        
        count = 0
        neibor_nums = []
        for number in numbers:
            number_value, left_ind, right_ind = number
            print(number_value)
            if right_ind == star_ind:
                print('cur line right')
                count += 1
                neibor_nums.append(number_value)
            if left_ind-1 == star_ind:
                print('cur line left')
                count += 1
                neibor_nums.append(number_value)
                
        if i > 0:
            numbers = found_numbers_list[i-1]
            for number in numbers:
                number_value, left_ind, right_ind = number
                print(number_value)
                if is_contian_star(star_ind, left_ind, right_ind):
                    print('prev line')
                    count += 1
                    neibor_nums.append(number_value)
        if i < n_row - 1:
            numbers = found_numbers_list[i+1]
            for number in numbers:
                number_value, left_ind, right_ind = number
                print(number_value)
                if is_contian_star(star_ind, left_ind, right_ind):
                    print('next line')
                    count += 1
                    neibor_nums.append(number_value)
        print('count',count)
        if count == 2:
            print(neibor_nums)
            new_sum_numbers += neibor_nums[0]*neibor_nums[1]
print(16345+451490)
# print(adjacent_numbers)
print(new_sum_numbers)
result = 0
print("Sum of all part numbers in the engine schematic:", result)
