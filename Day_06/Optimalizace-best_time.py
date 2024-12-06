from typing import List, Tuple, Set
from copy import deepcopy
from time import time
from functools import lru_cache, cached_property

class Pohybstrazce:
    def __init__(self, map_data: List[str]):
        self._map_data = tuple(tuple(row) for row in map_data)
        self.height = len(self._map_data)
        self.width = len(self._map_data[0])
        self.directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
        self.direction_symbols = ('^', '>', 'v', '<')
        
        self._initial_position = self._find_guard_position()
        self._initial_direction = self._find_guard_direction()
        self.map = None  # Pro ukládání aktuální mapy při simulaci
        self._guard_pos = self._initial_position
        self._direction = self._initial_direction
    
    @lru_cache(maxsize=None)
    def _find_guard_position(self) -> Tuple[int, int]:
        """Kešovaná verze nalezení pozice strážce."""
        for y in range(self.height):
            for x in range(self.width):
                if self._map_data[y][x] in self.direction_symbols:
                    return (y, x)
        raise ValueError("Strážce nebyl nalezen na mapě!")
    
    @lru_cache(maxsize=None)
    def _find_guard_direction(self) -> int:
        """Kešovaná verze nalezení směru strážce."""
        y, x = self._initial_position
        symbol = self._map_data[y][x]
        return self.direction_symbols.index(symbol)
    
    @property
    def pocatecni_pozice(self):
        return self._initial_position
    
    @property
    def guard_pos(self):
        return self._guard_pos
    
    @guard_pos.setter
    def guard_pos(self, value):
        self._guard_pos = value
    
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value):
        self._direction = value
    
    @lru_cache(maxsize=1024)
    def kontrola_pozice(self, pos: Tuple[int, int]) -> bool:
        y, x = pos
        return 0 <= y < self.height and 0 <= x < self.width
    
    def Najdi_dalsi_pozici(self) -> Tuple[int, int]:
        dy, dx = self.directions[self.direction]
        y, x = self.guard_pos
        return (y + dy, x + dx)

    def Najdi_dosazitelne_pozice(self) -> Set[Tuple[int, int]]:
        """Najde všechny pozice, kam se strážce může dostat bez překážek."""
        if hasattr(self, '_dosazitelne_pozice'):
            return self._dosazitelne_pozice
            
        dosazitelne = set()
        navstivene_stavy = set()
        
        self.guard_pos = self._initial_position
        self.direction = self._initial_direction
        
        while True:
            aktualni_stav = (self.guard_pos, self.direction)
            dosazitelne.add(self.guard_pos)
            
            if aktualni_stav in navstivene_stavy:
                break
                
            navstivene_stavy.add(aktualni_stav)
            
            next_pos = self.Najdi_dalsi_pozici()
            if not self.kontrola_pozice(next_pos):
                break
                
            next_y, next_x = next_pos
            if self._map_data[next_y][next_x] == '#':
                self.direction = (self.direction + 1) % 4
            else:
                self.guard_pos = next_pos
        
        self._dosazitelne_pozice = dosazitelne
        return dosazitelne

    def Simulace_kroku(self) -> bool:
        """Simuluje jeden krok strážce."""
        if self.map is None:
            self.map = [list(row) for row in self._map_data]
            
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
        dosazitelne_pozice = self.Najdi_dosazitelne_pozice()
        pozice_smycek = set()
        
        celkem_pozic = len(dosazitelne_pozice)
        zpracovano = 0
        cas_zacatek = time()
        
        print(f"Začínám hledat smyčky... Celkem dosažitelných pozic ke kontrole: {celkem_pozic}")
        
        for y, x in dosazitelne_pozice:
            zpracovano += 1
            
            if zpracovano % 10 == 0 or zpracovano == celkem_pozic:
                cas_nyni = time()
                uplynuly_cas = cas_nyni - cas_zacatek
                prumer_cas = uplynuly_cas / zpracovano
                zbyvajici_pozice = celkem_pozic - zpracovano
                odhadovany_cas = zbyvajici_pozice * prumer_cas
                
                print(f"Zpracováno: {zpracovano}/{celkem_pozic} " + 
                      f"({(zpracovano/celkem_pozic*100):.1f}%) " +
                      f"Nalezeno smyček: {len(pozice_smycek)} " +
                      f"Zbývající čas: {odhadovany_cas:.1f}s")
            
            if (y, x) == self.pocatecni_pozice or self._map_data[y][x] != '.':
                continue
            
            self.map = [list(row) for row in self._map_data]
            self.map[y][x] = 'O'
            self.guard_pos = self._initial_position
            self.direction = self._initial_direction
            
            if self.Detekce_smycky():
                pozice_smycek.add((y, x))
    
        celkovy_cas = time() - cas_zacatek
        print(f"\nHledání dokončeno za {celkovy_cas:.1f} sekund")
        print(f"Celkem nalezeno {len(pozice_smycek)} možných pozic pro smyčky")
        
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
    print("Načítám a zpracovávám vstupní data...")
    map_data = [line.strip() for line in input_data.strip().split('\n')]
    guard = Pohybstrazce(map_data)
    return len(guard.Najdi_pozice_smycek())

filename = "Day_06/input_06.txt"
print(f"Načítám soubor: {filename}")
input_data = nacti_data(filename)

if input_data:
    print("\nSpouštím řešení části 2...")
    result = hledani_reseni_cast2(input_data)
    print(f"\nVÝSLEDEK: Počet možných pozic pro vytvoření smyčky: {result}")
else:
    print("Nepodařilo se načíst vstupní data.")