from collections import defaultdict
from heapq import heappush, heappop
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass(frozen=True, order=True)
class State:
    x: int
    y: int
    direction: int  # 0=východ, 1=jih, 2=západ, 3=sever

def load_maze(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def solve_maze(maze: List[str]) -> int:
    # Najít start a cíl
    start_x = start_y = end_x = end_y = 0
    height = len(maze)
    width = len(maze[0])
    
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 'S':
                start_x, start_y = x, y
            elif maze[y][x] == 'E':
                end_x, end_y = x, y

    # Směry pohybu (východ, jih, západ, sever)
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    
    # Prioritní fronta pro Dijkstru: (cost, state)
    pq = [(0, 0, State(start_x, start_y, 0))]  # přidáno unikátní ID pro stabilní řazení
    costs = {}
    counter = 1  # pro generování unikátních ID
    
    while pq:
        cost, _, current_state = heappop(pq)
        
        # Pokud jsme tento stav už viděli s nižší cenou, přeskočíme ho
        if current_state in costs and cost >= costs[current_state]:
            continue
        
        costs[current_state] = cost
        
        # Jsme v cíli?
        if current_state.x == end_x and current_state.y == end_y:
            return cost
            
        # Pohyb vpřed
        new_x = current_state.x + dx[current_state.direction]
        new_y = current_state.y + dy[current_state.direction]
        if (0 <= new_x < width and 0 <= new_y < height and 
            maze[new_y][new_x] != '#'):
            new_state = State(new_x, new_y, current_state.direction)
            new_cost = cost + 1
            if new_state not in costs or new_cost < costs[new_state]:
                heappush(pq, (new_cost, counter, new_state))
                counter += 1
        
        # Otočení vlevo a vpravo
        for new_direction in [(current_state.direction - 1) % 4,
                            (current_state.direction + 1) % 4]:
            new_state = State(current_state.x, current_state.y, new_direction)
            new_cost = cost + 1000
            if new_state not in costs or new_cost < costs[new_state]:
                heappush(pq, (new_cost, counter, new_state))
                counter += 1

    return float('inf')

def main():
    # Načtení a řešení hlavního vstupu
    maze = load_maze('Day_16/input_16.txt')
    result = solve_maze(maze)
    print(f"Nejnižší možné skóre pro vstupní bludiště: {result}")

if __name__ == "__main__":
    main()