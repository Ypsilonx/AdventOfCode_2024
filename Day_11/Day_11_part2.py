from collections import defaultdict
from typing import Dict

def transform_zero(stone: str) -> list[str]:
    return ['1']

def split_even_digits(stone: str) -> list[str]:
    if len(stone) % 2 == 0:
        mid = len(stone) // 2
        left = str(int(stone[:mid]))
        right = str(int(stone[mid:]))
        return [left, right]
    return []

def multiply_by_2024(stone: str) -> list[str]:
    return [str(int(stone) * 2024)]

def transform_stone(stone: str) -> list[str]:
    if stone == '0':
        return transform_zero(stone)
    
    split_result = split_even_digits(stone)
    if split_result:
        return split_result
    
    return multiply_by_2024(stone)

def blink_once(stone_counts: Dict[str, int]) -> Dict[str, int]:
    new_counts = defaultdict(int)
    
    for stone, count in stone_counts.items():
        new_stones = transform_stone(stone)
        for new_stone in new_stones:
            new_counts[new_stone] += count
            
    return new_counts

def simulate_blinks(stones: list[str], num_blinks: int) -> int:
    stone_counts = defaultdict(int)
    for stone in stones:
        stone_counts[stone] += 1
    
    for i in range(num_blinks):
        stone_counts = blink_once(stone_counts)
        if (i + 1) % 5 == 0:
            total = sum(stone_counts.values())
            print(f"After {i + 1} blinks: {total} stones")
    
    return sum(stone_counts.values())

# Test
initial_stones = "5 127 680267 39260 0 26 3553 5851995".split()
result = simulate_blinks(initial_stones, 75)
print(f"Final number of stones: {result}")