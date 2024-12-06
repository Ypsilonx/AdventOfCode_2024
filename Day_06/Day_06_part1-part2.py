from typing import List, Tuple, Set

class Pohybstrazce:
    def __init__(self, map_data: List[str]):
        self.map = [list(row) for row in map_data]
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.direction_symbols = ['^', '>', 'v', '<']
        
        self.guard_pos = self.Najdi_strazce()
        self.direction = self.Najdi_pocatek_strazce()
        
    def Najdi_strazce(self) -> Tuple[int, int]:
        """Najde počáteční pozici strážce na mapě."""
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in '^>v<':
                    return (y, x)
        raise ValueError("Strážce nebyl nalezen na mapě!")
        
    def Najdi_pocatek_strazce(self) -> int:
        """Určí počáteční směr strážce podle symbolu."""
        symbol = self.map[self.guard_pos[0]][self.guard_pos[1]]
        return self.direction_symbols.index(symbol)
    
    def kontrola_pozice(self, pos: Tuple[int, int]) -> bool:
        """Zkontroluje, zda je pozice v rámci mapy."""
        y, x = pos
        return 0 <= y < self.height and 0 <= x < self.width
    
    def Najdi_dalsi_pozici(self) -> Tuple[int, int]:
        """Vypočítá další pozici na základě současného směru."""
        dy, dx = self.directions[self.direction]
        y, x = self.guard_pos
        return (y + dy, x + dx)
    
    def Simulace_pohybu(self) -> int:
        """Simuluje pohyb strážce a vrací počet navštívených pozic."""
        visited = {self.guard_pos}
        
        while True:
            next_pos = self.Najdi_dalsi_pozici()
            
            if not self.kontrola_pozice(next_pos):
                break
                
            next_y, next_x = next_pos
            if self.map[next_y][next_x] == '#':
                self.direction = (self.direction + 1) % 4
            else:
                self.guard_pos = next_pos
                visited.add(next_pos)
        
        return len(visited)

def nacti_data(filename: str) -> str:
    """Načte vstupní data ze souboru."""
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Soubor {filename} nebyl nalezen!")
        return ""
    except Exception as e:
        print(f"Nastala chyba při čtení souboru: {e}")
        return ""

def hledani_reseni(input_data: str) -> int:
    """Fce - pro nalezení výsledku."""
    map_data = [line.strip() for line in input_data.strip().split('\n')]
    
    guard = Pohybstrazce(map_data)
    return guard.Simulace_pohybu()

filename = "Day_06/input_06.txt"
input_data = nacti_data(filename)

if input_data:
    result = hledani_reseni(input_data)
    print(f"Počet navštívených pozic ze souboru {filename}: {result}")
else:
    print("Nepodařilo se načíst vstupní data.")

test_input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()

test_result = hledani_reseni(test_input)
print(f"Počet navštívených pozic pro testovací data: {test_result}")

# ___________________________________________________________________________

from typing import List, Tuple, Set
from copy import deepcopy

class Pohybstrazce:
    def __init__(self, map_data: List[str]):
        self.original_map = [list(row) for row in map_data]
        self.map = deepcopy(self.original_map)
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.direction_symbols = ['^', '>', 'v', '<']
        
        self.pocatecni_pozice = self.Najdi_strazce()
        self.guard_pos = self.pocatecni_pozice
        self.direction = self.Najdi_pocatek_strazce()
        
    def Najdi_strazce(self) -> Tuple[int, int]:
        """Najde počáteční pozici strážce na mapě."""
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in '^>v<':
                    return (y, x)
        raise ValueError("Strážce nebyl nalezen na mapě!")
        
    def Najdi_pocatek_strazce(self) -> int:
        """Určí počáteční směr strážce podle symbolu."""
        symbol = self.map[self.guard_pos[0]][self.guard_pos[1]]
        return self.direction_symbols.index(symbol)
    
    def kontrola_pozice(self, pos: Tuple[int, int]) -> bool:
        """Zkontroluje, zda je pozice v rámci mapy."""
        y, x = pos
        return 0 <= y < self.height and 0 <= x < self.width
    
    def Najdi_dalsi_pozici(self) -> Tuple[int, int]:
        """Vypočítá další pozici na základě současného směru."""
        dy, dx = self.directions[self.direction]
        y, x = self.guard_pos
        return (y + dy, x + dx)
    
    def Simulace_kroku(self) -> bool:
        """Simuluje jeden krok strážce."""
        next_pos = self.Najdi_dalsi_pozici()
        
        if not self.kontrola_pozice(next_pos):
            return False
            
        next_y, next_x = next_pos
        if self.map[next_y][next_x] in '#O':
            self.direction = (self.direction + 1) % 4
        else:
            self.guard_pos = next_pos
        
        return True

    def Detekce_smycky(self, max_kroku: int = 10000) -> bool:
        """Detekuje, zda se strážce dostal do smyčky."""
        navstivene_stavy = set()
        kroky = 0
        
        while kroky < max_kroku:
            aktualni_stav = (self.guard_pos, self.direction)
            
            if aktualni_stav in navstivene_stavy:
                return True
                
            navstivene_stavy.add(aktualni_stav)
            
            if not self.Simulace_kroku():
                return False
                
            kroky += 1
        
        return False

    def Najdi_pozice_smycek(self) -> Set[Tuple[int, int]]:
        """Najde všechny pozice, kde přidání překážky vytvoří smyčku."""
        pozice_smycek = set()
        
        for y in range(self.height):
            for x in range(self.width):
                if (y, x) == self.pocatecni_pozice or self.original_map[y][x] != '.':
                    continue
                
                self.map = deepcopy(self.original_map)
                self.map[y][x] = 'O'
                self.guard_pos = self.pocatecni_pozice
                self.direction = self.Najdi_pocatek_strazce()
                
                if self.Detekce_smycky():
                    pozice_smycek.add((y, x))
        
        return pozice_smycek

def nacti_data(filename: str) -> str:
    """Načte vstupní data ze souboru."""
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Soubor {filename} nebyl nalezen!")
        return ""
    except Exception as e:
        print(f"Nastala chyba při čtení souboru: {e}")
        return ""

def hledani_reseni_cast2(input_data: str) -> int:
    """Fce - pro nalezení výsledku druhé části."""
    map_data = [line.strip() for line in input_data.strip().split('\n')]
    guard = Pohybstrazce(map_data)
    return len(guard.Najdi_pozice_smycek())

filename = "Day_06/input_06.txt"
input_data = nacti_data(filename)

if input_data:
    result = hledani_reseni_cast2(input_data)
    print(f"Počet možných pozic pro vytvoření smyčky: {result}")
else:
    print("Nepodařilo se načíst vstupní data.")

test_input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip()

test_result = hledani_reseni_cast2(test_input)
print(f"Počet možných pozic pro testovací data: {test_result}")