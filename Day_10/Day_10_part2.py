from typing import List, Set, Dict, Tuple
from collections import defaultdict

def count_distinct_paths(grid: List[List[int]]) -> int:
    def is_valid(x: int, y: int) -> bool:
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])
    
    def get_next_positions(x: int, y: int) -> List[Tuple[int, int]]:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # vpravo, dolů, vlevo, nahoru
        current_height = grid[x][y]
        next_positions = []
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (is_valid(new_x, new_y) and 
                grid[new_x][new_y] == current_height + 1):
                next_positions.append((new_x, new_y))
        
        return next_positions

    def count_paths(x: int, y: int, memo: Dict[Tuple[int, int], int]) -> int:
        # Pokud jsme našli cestu k 9, započítáme ji
        if grid[x][y] == 9:
            return 1
            
        # Pokud jsme už tuto pozici počítali, vrátíme memoizovaný výsledek
        pos = (x, y)
        if pos in memo:
            return memo[pos]
            
        # Rekurzivně počítáme cesty pro všechny možné další kroky
        total_paths = 0
        for next_x, next_y in get_next_positions(x, y):
            total_paths += count_paths(next_x, next_y, memo)
            
        # Uložíme výsledek do memoizace a vrátíme ho
        memo[pos] = total_paths
        return total_paths

    total_rating = 0
    rows, cols = len(grid), len(grid[0])
    
    # Procházíme všechny trailheady (pozice s výškou 0)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                # Pro každý trailhead počítáme počet různých cest
                memo = {}  # Memoizace pro optimalizaci
                rating = count_paths(i, j, memo)
                total_rating += rating
                
    return total_rating

def parse_input(input_str: str) -> List[List[int]]:
    return [[int(char) for char in line] for line in input_str.strip().split('\n')]

# Test na příkladu ze zadání
test_input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

grid = parse_input(test_input)
result = count_distinct_paths(grid)
print(f"Výsledek pro testovací vstup: {result}")  # Mělo by vypsat 81