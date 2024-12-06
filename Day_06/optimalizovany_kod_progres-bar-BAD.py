import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Set
from copy import deepcopy
from time import time
import tqdm

class RychlePocitani:
    def __init__(self, map_data: List[str]):
        self.original_map = [list(row) for row in map_data]
        self.map = deepcopy(self.original_map)
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.direction_symbols = ['^', '>', 'v', '<']
        self.pocatecni_pozice = self.najdi_strazce()
        self.reachable_positions = set()
        self.found_loops = 0

    def najdi_strazce(self) -> Tuple[int, int]:
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in '^>v<':
                    return (y, x)
        raise ValueError("Strážce nebyl nalezen na mapě!")

    def najdi_dosazitelne_pozice(self):
        temp_map = deepcopy(self.original_map)
        guard_pos = self.pocatecni_pozice
        direction = self.direction_symbols.index(
            self.original_map[self.pocatecni_pozice[0]][self.pocatecni_pozice[1]]
        )
        
        self.reachable_positions = {guard_pos}
        steps = 0
        
        while steps < 1000:
            dy, dx = self.directions[direction]
            next_y, next_x = guard_pos[0] + dy, guard_pos[1] + dx
            
            if not (0 <= next_y < self.height and 0 <= next_x < self.width):
                break
                
            if temp_map[next_y][next_x] == '#':
                direction = (direction + 1) % 4
            else:
                guard_pos = (next_y, next_x)
                self.reachable_positions.add(guard_pos)
            
            steps += 1

    def simuluj_pohyb(self, pozice: Tuple[int, int]) -> bool:
        """Rychlá simulace pohybu bez vizualizace"""
        if pozice == self.pocatecni_pozice or self.original_map[pozice[0]][pozice[1]] != '.':
            return False

        temp_map = deepcopy(self.original_map)
        temp_map[pozice[0]][pozice[1]] = '#'  # Použijeme # místo O pro překážku
        
        guard_pos = self.pocatecni_pozice
        direction = self.direction_symbols.index(
            self.original_map[self.pocatecni_pozice[0]][self.pocatecni_pozice[1]]
        )
        
        visited_states = set()
        steps = 0
        
        while steps < 1000:
            current_state = (guard_pos, direction)
            if current_state in visited_states:
                return True
            
            visited_states.add(current_state)
            dy, dx = self.directions[direction]
            next_y, next_x = guard_pos[0] + dy, guard_pos[1] + dx
            
            if not (0 <= next_y < self.height and 0 <= next_x < self.width):
                return False
            
            if temp_map[next_y][next_x] == '#':
                direction = (direction + 1) % 4
            else:
                guard_pos = (next_y, next_x)
            
            steps += 1
        
        return False

    def najdi_smycky(self) -> int:
        """Najde všechny pozice pro smyčky s progress barem"""
        print("Hledám dosažitelné pozice...")
        start_time = time()
        self.najdi_dosazitelne_pozice()
        
        testovatelne_pozice = [(y, x) for y in range(self.height) for x in range(self.width)
                              if (y, x) in self.reachable_positions and 
                              self.original_map[y][x] == '.']
        
        print(f"Nalezeno {len(testovatelne_pozice)} dosažitelných pozic")
        print("Hledám smyčky...")
        
        for pozice in tqdm.tqdm(testovatelne_pozice):
            if self.simuluj_pohyb(pozice):
                self.found_loops += 1
        
        end_time = time()
        print(f"\nCelkový čas výpočtu: {end_time - start_time:.2f} sekund")
        return self.found_loops

def nacti_data(filename: str) -> List[str]:
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Soubor {filename} nebyl nalezen!")
        return []
    except Exception as e:
        print(f"Nastala chyba při čtení souboru: {e}")
        return []

def vyber_reseni():
    root = tk.Tk()
    root.title("Výběr způsobu řešení")

    def spust_vizualizaci():
        root.destroy()
        # Zde by byl váš původní kód pro vizualizaci
        print("Spouštím vizualizaci...")
        # Import a spuštění původní vizualizace

    def spust_rychle_reseni():
        root.destroy()
        print("Spouštím rychlé řešení...")
        
        # Test data
        test_input = [
            "....#.....",
            ".........#",
            "..........",
            "..#.......",
            ".......#..",
            "..........",
            ".#..^.....",
            "........#.",
            "#.........",
            "......#..."
        ]
        
        # Nejdřív test na vzorových datech
        print("\nTestuji na vzorových datech:")
        solver = RychlePocitani(test_input)
        result = solver.najdi_smycky()
        print(f"Výsledek pro testovací data: {result}")
        
        # Pak řešení pro skutečná data
        print("\nŘeším skutečná data:")
        file_data = nacti_data("Day_06/input_06.txt")
        if file_data:
            solver = RychlePocitani(file_data)
            result = solver.najdi_smycky()
            print(f"Výsledek pro vstupní data: {result}")
        else:
            print("Nepodařilo se načíst vstupní data!")

    tk.Label(root, text="Vyberte způsob řešení:").pack(pady=10)
    tk.Button(root, text="Spustit vizualizaci", command=spust_vizualizaci).pack(pady=5)
    tk.Button(root, text="Rychlé řešení (bez vizualizace)", command=spust_rychle_reseni).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    vyber_reseni()