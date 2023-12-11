#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 09:49:08 2023

@author: yuxuan
"""
import numpy as np

def calculate_points(card):
    winning_numbers, your_numbers = card.rstrip().split(" | ")
    winning_numbers = list(map(int, winning_numbers.split()))
    your_numbers = list(map(int, your_numbers.split()))


    n_points = 0
    score = 1
    print(your_numbers, '|', winning_numbers)
    for winning_number in winning_numbers:        
        if winning_number in your_numbers:
            n_points += 1
    
    return n_points

def calculate_scores(n_points):
    return 2 ** (n_points - 1) if n_points > 0 else 0 
    
    
def total_scores(cards):
    return sum(calculate_scores(calculate_points(card.split(':')[1])) for card in cards)

def total_cards(cards):
    n_card = len(cards)
    card_points = np.array([calculate_points(card.split(':')[1]) for card in cards])
    
    card_copies = np.ones(n_card)
    for i in range(n_card):
        card_below = card_points[i]
        card_copies[i+1:i+card_below+1] += card_copies[i]
        print(card_copies)
        
    sum_cards = np.sum(card_copies)
    return sum_cards
    
# Example input
file_path = '4_input_test.txt'
file_path = '4_input.txt'
with open(file_path, 'r') as file:
    content_list = file.readlines()

cards = content_list
result = total_scores(cards)
print(result)

result = total_cards(cards)
print(result)