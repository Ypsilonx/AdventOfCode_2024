from typing import List

def transform_zero(stone: str) -> List[str]:
    return ['1']

def split_even_digits(stone: str) -> List[str]:
    if len(stone) % 2 == 0:  
        mid = len(stone) // 2
        left = str(int(stone[:mid])) 
        right = str(int(stone[mid:]))  
        return [left, right]
    return [] 

def multiply_by_2024(stone: str) -> List[str]:
    return [str(int(stone) * 2024)]

def transform_stone(stone: str) -> List[str]:
    if stone == '0':
        return transform_zero(stone)
    
    split_result = split_even_digits(stone)
    if split_result:
        return split_result
    
    return multiply_by_2024(stone)

def blink_once(stones: List[str]) -> List[str]:
    new_stones = []
    for stone in stones:
        new_stones.extend(transform_stone(stone))
    return new_stones

def simulate_blinks(initial_stones: List[str], blinks: int) -> List[str]:
    current_stones = initial_stones
    for _ in range(blinks):
        current_stones = blink_once(current_stones)
    return current_stones

def parse_input(input_str: str) -> List[str]:
    """Převede vstupní řetězec na seznam kamenů"""
    return input_str.strip().split()

test_input = "5 127 680267 39260 0 26 3553 5851995"
stones = parse_input(test_input)
after_one_blink = blink_once(stones)
print(f"Počet kamenů po jednom mrknutí: {len(after_one_blink)}")
print(f"Kameny po jednom mrknutí: {' '.join(after_one_blink)}")

final_stones = simulate_blinks(stones, 5)
print(f"Počet kamenů po 25 mrknutích: {len(final_stones)}")