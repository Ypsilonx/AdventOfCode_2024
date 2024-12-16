from collections import deque, defaultdict
from typing import List, Set, Tuple, Dict

def load_maze(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def find_best_paths(maze: List[str]) -> Set[tuple[int, int]]:
    height = len(maze)
    width = len(maze[0])
    
    # Najít start a cíl
    start_x = start_y = end_x = end_y = 0
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 'S':
                start_x, start_y = x, y
            elif maze[y][x] == 'E':
                end_x, end_y = x, y

    # Směry pohybu
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # vpravo, dolů, vlevo, nahoru
    
    # BFS
    queue = deque([(start_x, start_y, [(start_x, start_y)])])
    visited = set()
    best_paths = []
    min_length = float('inf')
    
    while queue:
        x, y, path = queue.popleft()
        
        # Jsme v cíli?
        if x == end_x and y == end_y:
            path_length = len(path)
            if path_length < min_length:
                min_length = path_length
                best_paths = [path]
            elif path_length == min_length:
                best_paths.append(path)
            continue
            
        # Pokud je cesta už delší než nejlepší nalezená, ignorujeme ji
        if len(path) > min_length:
            continue
            
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            if (0 <= new_x < width and 0 <= new_y < height and 
                maze[new_y][new_x] != '#' and 
                (new_x, new_y) not in path):  # Vyhýbáme se cyklům
                new_path = path + [(new_x, new_y)]
                queue.append((new_x, new_y, new_path))

    # Shromáždit všechna unikátní políčka ze všech nejlepších cest
    path_tiles = set()
    for path in best_paths:
        path_tiles.update(path)
        
    return path_tiles

def visualize_paths(maze: List[str], path_tiles: Set[tuple[int, int]]) -> None:
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if (x, y) in path_tiles and maze[y][x] != '#':
                print('O', end='')
            else:
                print(maze[y][x], end='')
        print()

def main():
    maze = load_maze('Day_16/input_16.txt')
    path_tiles = find_best_paths(maze)
    print(f"Počet políček na nejlepších cestách: {len(path_tiles)}")
    print("\nVisualizace nejlepších cest (O = políčko na nejlepší cestě):")
    visualize_paths(maze, path_tiles)

if __name__ == "__main__":
    main()