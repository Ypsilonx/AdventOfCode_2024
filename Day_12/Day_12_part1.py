import tkinter as tk
from tkinter import ttk
from typing import List, Set, Tuple, Dict
from collections import defaultdict

class GardenVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analýza zahradních oblastí")
        self.CELL_SIZE = 15
        self.colors = {
            'A': '#FF9999', 'B': '#99FF99', 'C': '#9999FF', 'D': '#FFFF99', 
            'E': '#FF99FF', 'F': '#99FFFF', 'G': '#FFB366', 'H': '#66FFB3', 
            'I': '#B366FF', 'J': '#66B3FF', 'K': '#FFB3B3', 'L': '#B3FFB3',
            'M': '#B3B3FF', 'N': '#FFFFB3', 'O': '#FFB3FF', 'P': '#B3FFFF', 
            'Q': '#E6B3B3', 'R': '#B3E6B3', 'S': '#B3B3E6', 'T': '#E6E6B3', 
            'U': '#E6B3E6', 'V': '#B3E6E6', 'W': '#FFE6B3', 'X': '#E6FFB3',
            'Y': '#B3FFE6', 'Z': '#E6B3FF'
        }
        
        try:
            self.garden_map = self.read_garden_map("Day_12/input_12.txt")
            self.create_layout()
            self.regions = self.find_regions()
            self.analyze_garden()
            self.draw_garden()
        except Exception as e:
            tk.messagebox.showerror("Chyba", f"Chyba při načítání nebo analýze dat: {str(e)}")

    def create_layout(self):
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Levý panel
        left_frame = ttk.Frame(main_frame)
        main_frame.add(left_frame)

        # Ovládací prvky
        control_frame = ttk.Frame(left_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Velikost buněk:").pack(side=tk.LEFT, padx=5)
        self.size_scale = ttk.Scale(
            control_frame,
            from_=5,
            to=30,
            orient=tk.HORIZONTAL,
            value=self.CELL_SIZE,
            command=self.update_cell_size
        )
        self.size_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Canvas se scrollbary
        canvas_frame = ttk.Frame(left_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        self.h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=800,
            height=600,
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set,
            bg='white'
        )
        
        self.v_scrollbar.config(command=self.canvas.yview)
        self.h_scrollbar.config(command=self.canvas.xview)
        
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Pravý panel
        right_frame = ttk.Frame(main_frame)
        main_frame.add(right_frame)

        # Tabulka
        columns = ('Region', 'Plocha', 'Obvod', 'Strany', 'Cena1', 'Cena2')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        
        self.tree.heading('Region', text='Region')
        self.tree.heading('Plocha', text='Plocha')
        self.tree.heading('Obvod', text='Obvod')
        self.tree.heading('Strany', text='Strany')
        self.tree.heading('Cena1', text='Cena (P1)')
        self.tree.heading('Cena2', text='Cena (P2)')
        
        for col in columns:
            self.tree.column(col, width=70)
        
        tree_scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Celkové ceny
        self.total_frame = ttk.Frame(right_frame)
        self.total_frame.pack(fill=tk.X, pady=10)
        
        self.total_label1 = ttk.Label(self.total_frame, text="Celková cena (Part 1): 0")
        self.total_label1.pack()
        
        self.total_label2 = ttk.Label(self.total_frame, text="Celková cena (Part 2): 0")
        self.total_label2.pack()

    def count_sides(self, region: Set[Tuple[int, int]], plant: str) -> int:
        """Spočítá počet souvislých stran regionu pro Part 2"""
        # Nejdřív najdeme všechny hraniční buňky a jejich strany
        border_cells = set()
        for x, y in region:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in region:
                    if (nx < 0 or ny < 0 or 
                        ny >= len(self.garden_map) or 
                        nx >= len(self.garden_map[0]) or
                        self.garden_map[ny][nx] != plant):
                        border_cells.add((x, y))
        
        # Funkce pro nalezení souvislé strany začínající v daném bodě a směru
        def trace_side(start_x: int, start_y: int, direction: str) -> Set[Tuple[int, int]]:
            visited = set()
            current = (start_x, start_y)
            side = {current}
            
            # Mapování směrů na offsety
            if direction == 'H':  # horizontální
                next_moves = [(1, 0), (-1, 0)]
                check_dirs = [(0, 1), (0, -1)]
            else:  # vertikální
                next_moves = [(0, 1), (0, -1)]
                check_dirs = [(1, 0), (-1, 0)]
            
            while True:
                x, y = current
                found_next = False
                
                # Kontrola, zda jsme stále na hranici
                is_border = False
                for dx, dy in check_dirs:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in region:
                        if (nx < 0 or ny < 0 or 
                            ny >= len(self.garden_map) or 
                            nx >= len(self.garden_map[0]) or
                            self.garden_map[ny][nx] != plant):
                            is_border = True
                            break
                
                if not is_border:
                    break
                    
                # Hledání další buňky v této straně
                for dx, dy in next_moves:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in border_cells and (nx, ny) not in visited:
                        # Kontrola, zda je nová buňka součástí stejné strany
                        is_same_side = False
                        for check_dx, check_dy in check_dirs:
                            check_x, check_y = nx + check_dx, ny + check_dy
                            if (check_x, check_y) not in region:
                                if (check_x < 0 or check_y < 0 or 
                                    check_y >= len(self.garden_map) or 
                                    check_x >= len(self.garden_map[0]) or
                                    self.garden_map[check_y][check_x] != plant):
                                    is_same_side = True
                                    break
                        
                        if is_same_side:
                            current = (nx, ny)
                            visited.add(current)
                            side.add(current)
                            found_next = True
                            break
                
                if not found_next:
                    break
            
            return side
        
        # Najdeme všechny souvislé strany
        used_cells = set()
        sides = 0
        
        for x, y in border_cells:
            if (x, y) in used_cells:
                continue
                
            # Zkusíme začít horizontální stranu
            horizontal_side = trace_side(x, y, 'H')
            if len(horizontal_side) > 0:
                sides += 1
                used_cells.update(horizontal_side)
                continue
                
            # Zkusíme začít vertikální stranu
            vertical_side = trace_side(x, y, 'V')
            if len(vertical_side) > 0:
                sides += 1
                used_cells.update(vertical_side)
                continue
                
            # Pokud buňka není součástí delší strany, je to samostatná strana
            if (x, y) not in used_cells:
                sides += 1
                used_cells.add((x, y))
        
        return sides

    def analyze_garden(self):
        """Analyzuje zahradu a aktualizuje UI s oběma metodami výpočtu"""
        total_price1 = 0  # Part 1
        total_price2 = 0  # Part 2
        self.tree.delete(*self.tree.get_children())
        
        region_count = 1
        for plant, plant_regions in self.regions.items():
            for region in plant_regions:
                area = len(region)
                perimeter = self.calculate_perimeter(region, plant)
                sides = self.count_sides(region, plant)
                price1 = area * perimeter  # Part 1
                price2 = area * sides      # Part 2
                total_price1 += price1
                total_price2 += price2
                
                self.tree.insert('', 'end',
                               values=(f"{plant}-{region_count}", 
                                     area, perimeter, sides, price1, price2))
                region_count += 1
        
        self.total_label1.config(text=f"Celková cena (Part 1): {total_price1}")
        self.total_label2.config(text=f"Celková cena (Part 2): {total_price2}")

    # Ostatní metody zůstávají stejné jako v předchozí verzi
    def update_cell_size(self, event=None):
        self.CELL_SIZE = int(self.size_scale.get())
        self.draw_garden()
    
    def read_garden_map(self, filename: str) -> List[str]:
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()]
    
    def find_regions(self) -> dict:
        height = len(self.garden_map)
        width = len(self.garden_map[0])
        visited = set()
        regions = defaultdict(list)
        
        def flood_fill(x: int, y: int, plant: str) -> Set[Tuple[int, int]]:
            if (x, y) in visited or self.garden_map[y][x] != plant:
                return set()
            
            region = {(x, y)}
            visited.add((x, y))
            stack = [(x, y)]
            
            while stack:
                curr_x, curr_y = stack.pop()
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_x, new_y = curr_x + dx, curr_y + dy
                    if (0 <= new_x < width and 0 <= new_y < height and
                            (new_x, new_y) not in visited and
                            self.garden_map[new_y][new_x] == plant):
                        visited.add((new_x, new_y))
                        region.add((new_x, new_y))
                        stack.append((new_x, new_y))
            
            return region

        for y in range(height):
            for x in range(width):
                if (x, y) not in visited:
                    plant = self.garden_map[y][x]
                    region = flood_fill(x, y, plant)
                    if region:
                        regions[plant].append(region)
        
        return regions
    
    def calculate_perimeter(self, region: Set[Tuple[int, int]], plant: str) -> int:
        perimeter = 0
        for x, y in region:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in region:
                    if (nx < 0 or ny < 0 or 
                        ny >= len(self.garden_map) or 
                        nx >= len(self.garden_map[0]) or
                        self.garden_map[ny][nx] != plant):
                        perimeter += 1
        return perimeter
    
    def draw_garden(self):
        self.canvas.delete('all')
        
        width = len(self.garden_map[0]) * self.CELL_SIZE
        height = len(self.garden_map) * self.CELL_SIZE
        
        self.canvas.configure(scrollregion=(0, 0, width, height))
        
        font_size = max(int(self.CELL_SIZE / 2), 1)
        for y, row in enumerate(self.garden_map):
            for x, plant in enumerate(row):
                x1 = x * self.CELL_SIZE
                y1 = y * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.colors.get(plant, '#FFFFFF'),
                    outline='gray'
                )
                if self.CELL_SIZE >= 10:
                    self.canvas.create_text(
                        x1 + self.CELL_SIZE/2,
                        y1 + self.CELL_SIZE/2,
                        text=plant,
                        font=('TkDefaultFont', font_size)
                    )

def main():
    root = tk.Tk()
    app = GardenVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()