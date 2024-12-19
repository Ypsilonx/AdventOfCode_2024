from collections import deque
from dataclasses import dataclass
import itertools
from typing import List, Set, Tuple, Optional
import heapq

@dataclass(frozen=True, order=True)  # Přidáno order=True pro podporu porovnávání
class Point:
    x: int
    y: int
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def manhattan_distance(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

class MemoryGrid:
    def __init__(self, size: int, corrupted_bytes: List[str]):
        self.size = size
        self.corrupted: Set[Point] = set()
        self.process_corrupted_bytes(corrupted_bytes)
        
    def process_corrupted_bytes(self, corrupted_bytes: List[str]) -> None:
        """Zpracuje seznam souřadnic poškozených bytů."""
        for line in corrupted_bytes:
            if not line.strip():
                continue
            x, y = map(int, line.strip().split(','))
            self.corrupted.add(Point(x, y))
    
    def is_valid(self, point: Point) -> bool:
        """Kontroluje, zda je bod v rámci mřížky a není poškozený."""
        return (0 <= point.x < self.size and 
                0 <= point.y < self.size and 
                point not in self.corrupted)

    def find_shortest_path(self, start: Point, end: Point) -> Optional[List[Point]]:
        """Najde nejkratší cestu pomocí A* algoritmu."""
        directions = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]
        
        # Změněna struktura pro heapq - používáme tuple (f_score, id(path), cost, current, path)
        # přidáno id(path) pro zajištění unikátního porovnání když f_score jsou stejné
        open_set = [(0 + start.manhattan_distance(end), id([start]), 0, start, [start])]
        closed_set = set()
        
        while open_set:
            _, _, cost, current, path = heapq.heappop(open_set)
            
            if current == end:
                return path
                
            if current in closed_set:
                continue
                
            closed_set.add(current)
            
            for direction in directions:
                next_point = current + direction
                if self.is_valid(next_point) and next_point not in closed_set:
                    new_cost = cost + 1
                    new_path = path + [next_point]
                    priority = new_cost + next_point.manhattan_distance(end)
                    heapq.heappush(open_set, (priority, id(new_path), new_cost, next_point, new_path))
        
        return None

    def visualize(self, path: Optional[List[Point]] = None) -> str:
        """Vytvoří textovou reprezentaci mřížky s cestou."""
        result = []
        path_set = set(path) if path else set()
        
        for y in range(self.size):
            row = []
            for x in range(self.size):
                point = Point(x, y)
                if point in self.corrupted:
                    row.append('#')
                elif point in path_set:
                    row.append('O')
                else:
                    row.append('.')
            result.append(''.join(row))
        
        return '\n'.join(result)

def solve_memory_escape(input_data: str, grid_size: int = 7) -> int:
    """Hlavní funkce pro řešení úlohy."""
    lines = [line.strip() for line in input_data.splitlines() if line.strip()]
    grid = MemoryGrid(grid_size, lines[:1024])  # Simulujeme prvních 1024 bytů
    
    start = Point(0, 0)
    end = Point(grid_size - 1, grid_size - 1)
    
    path = grid.find_shortest_path(start, end)
    if path is None:
        return -1  # Cesta neexistuje
        
    return len(path) - 1  # Odečteme 1, protože počítáme kroky, ne body

if __name__ == "__main__":
    # Test na vzorovém příkladu
    test_input = """
    5,4
    4,2
    4,5
    3,0
    2,1
    6,3
    2,4
    1,5
    0,6
    3,3
    2,6
    5,1
    """

    grid = MemoryGrid(7, test_input.strip().splitlines())
    path = grid.find_shortest_path(Point(0, 0), Point(6, 6))
    print("Vizualizace cesty:")
    print(grid.visualize(path))
    print(f"Počet kroků: {len(path) - 1}")