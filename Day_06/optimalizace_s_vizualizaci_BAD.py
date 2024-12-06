import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Set
from copy import deepcopy
from time import sleep

class VizualizaceStrazce:
    def __init__(self, master, map_data: List[str], cell_size=30):
        self.master = master
        self.cell_size = cell_size
        self.original_map = [list(row) for row in map_data]
        self.map = deepcopy(self.original_map)
        self.height = len(self.map)
        self.width = len(self.map[0])
        
        # Inicializace proměnných
        self.pause_simulation = False
        self.found_loops = 0
        self.current_test_pos = (0, 0)
        self.reachable_positions = set()
        
        # Nastavení okna
        self.master.title("Vizualizace pohybu strážce (Optimalizovaná verze)")
        
        # Vytvoření rámců
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.info_frame = tk.Frame(master)
        self.info_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Informační prvky
        self.info_label = tk.Label(self.info_frame, text="Testování pozice: 0,0")
        self.info_label.pack(side=tk.LEFT, padx=5)
        
        self.found_label = tk.Label(self.info_frame, text="Nalezené smyčky: 0")
        self.found_label.pack(side=tk.LEFT, padx=5)
        
        self.reachable_label = tk.Label(self.info_frame, text="Dosažitelné pozice: 0")
        self.reachable_label.pack(side=tk.LEFT, padx=5)
        
        # Inicializace směrů a symbolů
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
            'X': 'lightgreen',
            'R': 'lightyellow'
        }
        
        # Vytvoření ovládacích prvků a canvasu
        self.create_controls()
        self.create_scrollable_canvas()
        
        # Počáteční nalezení dosažitelných pozic
        self.find_reachable_positions()
        self.vykresli_mapu()

    def toggle_pause(self):
        """Přepíná mezi pauzou a pokračováním simulace"""
        self.pause_simulation = not self.pause_simulation
        self.pause_button.config(text="Pokračovat" if self.pause_simulation else "Pauza")

    def create_controls(self):
        """Vytvoří ovládací prvky"""
        self.start_button = tk.Button(self.control_frame, text="Spustit simulaci",
                                    command=self.spust_simulaci)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.control_frame, text="Pauza",
                                    command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.speed_var = tk.DoubleVar(value=0.1)
        self.speed_scale = tk.Scale(self.control_frame, from_=0, to=1.0,
                                  resolution=0.1, orient=tk.HORIZONTAL,
                                  label="Rychlost", variable=self.speed_var)
        self.speed_scale.pack(side=tk.RIGHT, padx=5)

    def create_scrollable_canvas(self):
        """Vytvoří scrollovatelný canvas"""
        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        canvas_width = min(self.width * self.cell_size, 800)
        canvas_height = min(self.height * self.cell_size, 600)
        self.canvas = tk.Canvas(self.canvas_frame, 
                              width=canvas_width, 
                              height=canvas_height,
                              scrollregion=(0, 0, 
                                          self.width * self.cell_size,
                                          self.height * self.cell_size),
                              yscrollcommand=self.v_scrollbar.set,
                              xscrollcommand=self.h_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.v_scrollbar.config(command=self.canvas.yview)
        self.h_scrollbar.config(command=self.canvas.xview)

    def najdi_strazce(self) -> Tuple[int, int]:
        """Najde počáteční pozici strážce"""
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in '^>v<':
                    return (y, x)
        raise ValueError("Strážce nebyl nalezen na mapě!")

    def vykresli_mapu(self):
        """Vykreslí aktuální stav mapy"""
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell_type = self.map[y][x]
                color = self.colors.get(cell_type, 'white')
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                
                if cell_type in '^>v<X':
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=cell_type,
                        font=('Arial', int(self.cell_size/2))
                    )
        
        self.canvas.update()

    def find_reachable_positions(self):
        """Najde všechny dosažitelné pozice"""
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
                temp_map[next_y][next_x] = 'R'
            
            steps += 1
        
        self.reachable_label.config(text=f"Dosažitelné pozice: {len(self.reachable_positions)}")
        
        for y, x in self.reachable_positions:
            if self.original_map[y][x] == '.':
                self.map[y][x] = 'R'

    def test_pozice(self, pos: Tuple[int, int]):
        """Testuje jednu pozici pro vytvoření smyčky"""
        while self.pause_simulation:
            self.master.update()
            sleep(0.1)
            
        y, x = pos
        self.current_test_pos = pos
        self.info_label.config(text=f"Testování pozice: {y},{x}")
        
        if (y, x) == self.pocatecni_pozice or self.original_map[y][x] != '.':
            return
        
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
        
        while steps < 1000:
            while self.pause_simulation:
                self.master.update()
                sleep(0.1)
                
            current_state = (guard_pos, direction)
            if current_state in visited_states:
                return True
            
            visited_states.add(current_state)
            
            dy, dx = self.directions[direction]
            next_y, next_x = guard_pos[0] + dy, guard_pos[1] + dx
            
            if not (0 <= next_y < self.height and 0 <= next_x < self.width):
                return False
            
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
        """Spustí simulaci pouze pro dosažitelné pozice"""
        self.start_button.config(state=tk.DISABLED)
        tested = 0
        total = len(self.reachable_positions)
        
        for y in range(self.height):
            for x in range(self.width):
                if (y, x) in self.reachable_positions and self.original_map[y][x] == '.':
                    tested += 1
                    self.info_label.config(text=f"Testování pozice: {y},{x} ({tested}/{total})")
                    self.test_pozice((y, x))
                    
        self.start_button.config(state=tk.NORMAL)

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

def vyber_data():
    root = tk.Tk()
    root.title("Výběr dat")
    
    def spust_vizualizaci_test():
        root.destroy()
        main_root = tk.Tk()
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
        app = VizualizaceStrazce(main_root, test_input)
        main_root.mainloop()
    
    def spust_vizualizaci_soubor():
        root.destroy()
        main_root = tk.Tk()
        file_data = nacti_data("Day_06/input_06.txt")
        if file_data:
            app = VizualizaceStrazce(main_root, file_data)
            main_root.mainloop()
        else:
            print("Nepodařilo se načíst data ze souboru!")
    
    tk.Label(root, text="Vyberte zdroj dat pro vizualizaci:").pack(pady=10)
    tk.Button(root, text="Testovací data", command=spust_vizualizaci_test).pack(pady=5)
    tk.Button(root, text="Data ze souboru", command=spust_vizualizaci_soubor).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    vyber_data()