#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 14:02:52 2023

@author: yuxuan
"""
import numpy as np
import math
import concurrent.futures
from numba import jit, prange

# def decode_mappings(mappings):
#     decoded_mappings = dict()
#     for mapping in mappings:
#         for i_mapping in mapping:
#             # print(i_mapping)
#             target_start, source_start, r = mapping
#             for i in range(r):
#                 decoded_mappings[source_start+i] = target_start+i
#     return decoded_mappings

# def find_target(seed, mappings):
#     target = seed if seed not in mappings.keys() else mappings[seed]
#     # print(target)
#     return target

# def apply_mappings(seed, mappings):
#     location = float('inf')
#     source = seed
#     for mapping in mappings:
#         source = find_target(source, decode_mappings(mapping))
    # 
    # return source
def get_seeds(seeds_range):
    seeds = []
    n_pair = len(seeds_range)//2    
    for i in range(n_pair):
        seeds.extend(list(range(seeds_range[2*i],seeds_range[2*i]+seeds_range[2*i+1])))
    return seeds


def apply_mappings(seed, mappings):
    current_mapping = seed
    for mapping in mappings:
        dest_start, source_start, length = mapping
        # print(current_mapping, source_start, source_start + length)
        if current_mapping >= source_start and current_mapping < source_start + length:
            # print('~~~',current_mapping, (current_mapping - source_start))
            current_mapping = dest_start + (current_mapping - source_start)
            break
    return current_mapping

@jit(nopython=True, parallel=True,fastmath=True)
def apply_mappings_optimized(seeds, mappings):
    current_mappings = seeds.copy()
    # current_mappings = seeds
    
    # current_mappings = np.arrange(seeds[0], seeds[-1]+1)
    
    for i in prange(len(mappings)):    
        dest_start, source_start, length = mappings[i]
        indices = (seeds >= source_start) & (seeds < source_start + length)
        current_mappings[indices] = dest_start + (seeds[indices] - source_start)
    
    return current_mappings

def find_lowest_location_(seed_start, seed_end, mappings):
    i_seed = np.arange(seed_start, seed_end)
    for mapping in mappings:
        i_seed = apply_mappings_optimized(i_seed, np.array(mapping))
    return i_seed


def find_lowest_location(seeds, mappings):
    # seeds = seeds[:2]
    # print(seeds)
    n_pair = len(seeds)//2    
    min_location = float('inf')
    min_location_all = float('inf')
    for i in range(n_pair):        
        # print(i,n_pair)
        # for seed in range(seeds[2*i],seeds[2*i]+seeds[2*i+1]):
        #     # print(seed)
        #     final_location = seed
        #     # print('!!!',seed)
        #     for mapping in mappings:            
        #         final_location = apply_mappings(final_location, mapping)
        #         # print(final_location)
        #     min_location = min([final_location, min_location])    
        
        # seed_np = np.array(range(seeds[2*i],seeds[2*i]+seeds[2*i+1]))
        
        num_seed = seeds[2*i+1]
        batch_size = 10000000
        # print(num_seed / batch_size, math.ceil(num_seed / batch_size))
        n_batch = math.ceil(num_seed / batch_size)
        # print(num_seed)
        pair_end = seeds[2*i]+seeds[2*i+1]
        results = []
        
        # with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for i_batch in range(n_batch):
            print(i,n_pair, i_batch, n_batch)
            seed_start = seeds[2*i]+i_batch*batch_size
            seed_end = seeds[2*i]+(i_batch+1)*batch_size
            
            seed_end = seed_end if seed_end <= pair_end else pair_end            
            i_seed = find_lowest_location_(seed_start, seed_end, mappings)
            min_location = np.min(i_seed)
            min_location_all = min(min_location, min_location_all)
                
                # results.append(executor.submit(find_lowest_location_, seed_start, seed_end, mappings))
               
            # for i_batch in range(n_batch):
            #     print("wait results: ", i_batch, n_batch)
            #     i_seed = np.min(results[i_batch].result())
                
            #     min_location = np.min(i_seed)
            #     min_location_all = min(min_location, min_location_all)
            # print(seed_np)
        
    return min_location_all


# def find_lowest_location(seeds, mappings):
#     locations = []
#     for seed in seeds:
#         print(seed)
#         location = apply_mappings(seed, mappings)
#         locations.append(location)
    
#     return min(locations)
    # lowest_location = float('inf')
    # for seed in seeds:
    #     final_location = apply_mappings(seed, mappings[-1][::-1])
    #     for mapping in reversed(mappings[:-1]):
    #         final_location = apply_mappings(final_location, [mapping])
    #     lowest_location = min(lowest_location, final_location)
    # return lowest_location

def read_input(file_name):
    # Read the data from the text
    with open(file_name, 'r') as file:
        data = file.read()
    
    # Split the data into lines
    lines = data.split('\n')
    
    # Extract seeds
    seeds_line = lines[0].split(': ')[1]
    seeds = list(map(int, seeds_line.split()))
    
    # Extract mappings
    mappings = []
    current_mapping = []
    find_first_map = False
    for line in lines[1:]:
        if not line:
            continue  # Skip empty lines
            
        if not find_first_map and line.endswith('map:'):
            find_first_map = True
            continue      
        
            
        if line.endswith(' map:'):
            if current_mapping:
                mappings.append(current_mapping)
            current_mapping = []
        else:
            mapping = list(map(int, line.split()))
            current_mapping.append(mapping)
    
    # Add the last mapping
    if current_mapping:
        print("!!!!!!!!!!!!!!!!!!")
        mappings.append(current_mapping)
    
    # Print the extracted data
        
    return seeds, mappings

# Define the almanac data
seeds = [79, 14, 55, 13]
seed_to_soil_map = [
    [50, 98, 2],
    [52, 50, 48]
]
soil_to_fertilizer_map = [
    [0, 15, 37],
   [37, 52, 2],
    [39, 0, 15]
]
fertilizer_to_water_map = [
    [49, 53, 8],
    [0, 11, 42],
    [42, 0, 7],
   [57, 7, 4]
]
water_to_light_map = [
    [88, 18, 7],
    [18, 25, 70]
]
light_to_temperature_map = [
    [45, 77, 23],
    [81, 45, 19],
    [68, 64, 13]
]
temperature_to_humidity_map = [
    [0, 69, 1],
    [1, 0, 69]
]
humidity_to_location_map = [
    [60, 56, 37],
    [56, 93, 4]
]

# Organize the mappings
mappings = [
    seed_to_soil_map,
    soil_to_fertilizer_map,
    fertilizer_to_water_map,
    water_to_light_map,
    light_to_temperature_map,
    temperature_to_humidity_map,
    humidity_to_location_map
]

# Find the lowest location number
# result = find_lowest_location(seeds, mappings)
# print("Lowest location number:", result)

# file_names = "5_input.txt"
# seeds, mappings = read_input(file_names)
#########################
#######  slow  ##########
#########################
# seeds = seeds
# result = find_lowest_location(seeds, mappings)
# print("Lowest location number:", result)
#########################


#########################
#######  quick  #########
#########################

def find_location_fast_one(seed_pair, mappings):
    lowest_locations = []    
    seed_pair_ = seed_pair
    
    temp_locs = []
    
    for target, src, length in mappings:
        
        
        (src_start, src_end) = src, src+length
        seed_left = []
        while seed_pair_:            
            i_seed_pair = seed_pair_.pop() 
            seed_start, seed_end = i_seed_pair
            # print('!!', target,src,length)
            
            left = (seed_start, min(src_start, seed_end))
            middle = (max(seed_start,src_start), min(src_end, seed_end))
            right = (max(seed_start, src_end), seed_end )
            
                        
            if left[0] < left[1]:
                seed_left.append(left)
            if middle[0] < middle[1]:
                # print("hhhhhh")                
                offset = -src_start+target
                temp_locs.append((middle[0]+offset, middle[1]+offset))
            if right[0] < right[1]:
                seed_left.append(right)
                
            # print('111~~~',seed_left)
            # print('222~~~',temp_locs)
        
        seed_pair_ = seed_left 
        
    return seed_pair_ + temp_locs

def find_location_fast(seed_pair, mappings):
    
    locations =[]
    n_pair = len(seed_pair)//2
    count = 1
    for i_pair in zip(seed_pair[::2], seed_pair[1::2]):
        i_pair = [(i_pair[0], i_pair[0]+i_pair[1])]
        print(count, n_pair)
        count +=1
        for mapping in mappings:
            i_pair = find_location_fast_one(i_pair, mapping)
        locations.extend(min(i_pair))
    print(min(locations))
        
    
result = find_location_fast(seeds, mappings)
print("Lowest location number:", result)

file_names = "5_input.txt"
seeds, mappings = read_input(file_names)
result = find_location_fast(seeds, mappings)
print("Lowest location number:", result)