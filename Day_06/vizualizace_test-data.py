import tkinter as tk
from typing import List, Tuple, Set
from copy import deepcopy
from time import sleep

class VizualizaceStrazce:
    def __init__(self, master, map_data: List[str], cell_size=40):
        self.master = master
        self.cell_size = cell_size
        self.original_map = [list(row) for row in map_data]
        self.map = deepcopy(self.original_map)
        self.height = len(self.map)
        self.width = len(self.map[0])
        
        # Nastavení okna
        self.master.title("Vizualizace pohybu strážce")
        
        # Vytvoření rámce pro ovládací prvky
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Informační panel
        self.info_label = tk.Label(self.control_frame, text="Testování pozice: 0,0")
        self.info_label.pack(side=tk.LEFT, padx=5)
        
        self.found_label = tk.Label(self.control_frame, text="Nalezené smyčky: 0")
        self.found_label.pack(side=tk.LEFT, padx=5)
        
        # Tlačítka pro ovládání
        self.speed_var = tk.DoubleVar(value=0.1)
        self.speed_scale = tk.Scale(self.control_frame, from_=0, to=1.0, 
                                  resolution=0.1, orient=tk.HORIZONTAL,
                                  label="Rychlost", variable=self.speed_var)
        self.speed_scale.pack(side=tk.RIGHT, padx=5)
        
        # Canvas pro mapu
        canvas_width = self.width * cell_size
        canvas_height = self.height * cell_size
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        
        # Inicializace pohybu strážce
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.direction_symbols = ['^', '>', 'v', '<']
        self.pocatecni_pozice = self.najdi_strazce()
        
        # Barvy pro vizualizaci
        self.colors = {
            '.': 'white',
            '#': 'gray',
            'O': 'red',
            '^': 'blue',
            '>': 'blue',
            'v': 'blue',
            '<': 'blue',
            'X': 'lightgreen'
        }
        
        self.found_loops = 0
        self.current_test_pos = (0, 0)
        
        # První vykreslení mapy
        self.vykresli_mapu()
        
    def najdi_strazce(self) -> Tuple[int, int]:
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in '^>v<':
                    return (y, x)
        return (0, 0)
    
    def vykresli_mapu(self):
        """Vykreslí aktuální stav mapy"""
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Vykreslení buňky
                cell_type = self.map[y][x]
                color = self.colors.get(cell_type, 'white')
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                
                # Vykreslení symbolu
                if cell_type in '^>v<X':
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=cell_type,
                        font=('Arial', int(self.cell_size/2))
                    )
        
        self.canvas.update()
    
    def test_pozice(self, pos: Tuple[int, int]):
        """Testuje jednu pozici pro vytvoření smyčky"""
        y, x = pos
        self.current_test_pos = pos
        self.info_label.config(text=f"Testování pozice: {y},{x}")
        
        if (y, x) == self.pocatecni_pozice or self.original_map[y][x] != '.':
            return
        
        # Reset mapy a přidání nové překážky
        self.map = deepcopy(self.original_map)
        self.map[y][x] = 'O'
        self.vykresli_mapu()
        sleep(self.speed_var.get())
        
        if self.simuluj_pohyb():
            self.found_loops += 1
            self.found_label.config(text=f"Nalezené smyčky: {self.found_loops}")
    
    def simuluj_pohyb(self) -> bool:
        """Simuluje pohyb strážce a hledá smyčku"""
        guard_pos = self.pocatecni_pozice
        direction = self.direction_symbols.index(
            self.original_map[self.pocatecni_pozice[0]][self.pocatecni_pozice[1]]
        )
        visited_states = set()
        steps = 0
        
        while steps < 1000:  # Maximální počet kroků
            current_state = (guard_pos, direction)
            if current_state in visited_states:
                return True
            
            visited_states.add(current_state)
            
            # Výpočet další pozice
            dy, dx = self.directions[direction]
            next_y, next_x = guard_pos[0] + dy, guard_pos[1] + dx
            
            # Kontrola platnosti pozice
            if not (0 <= next_y < self.height and 0 <= next_x < self.width):
                return False
            
            # Pohyb strážce
            if self.map[next_y][next_x] in '#O':
                direction = (direction + 1) % 4
            else:
                guard_pos = (next_y, next_x)
                self.map[next_y][next_x] = 'X'
                self.vykresli_mapu()
                sleep(self.speed_var.get() / 2)
            
            steps += 1
        
        return False
    
    def spust_simulaci(self):
        """Spustí kompletní simulaci pro všechny pozice"""
        for y in range(self.height):
            for x in range(self.width):
                self.test_pozice((y, x))

# Vytvoření hlavního okna a spuštění vizualizace
def spust_vizualizaci(map_data: List[str]):
    root = tk.Tk()
    app = VizualizaceStrazce(root, map_data)
    
    # Tlačítko pro spuštění simulace
    start_button = tk.Button(app.control_frame, text="Spustit simulaci",
                           command=app.spust_simulaci)
    start_button.pack(side=tk.LEFT, padx=5)
    
    root.mainloop()

# Testovací data
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
""".strip().split('\n')

# Spuštění vizualizace
if __name__ == "__main__":
    spust_vizualizaci(test_input)