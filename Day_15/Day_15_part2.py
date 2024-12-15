import pygame
import sys
import time
from typing import List, Tuple, Set

def load_moves_sequence(filename: str) -> str:
    """Načte sekvenci pohybů ze souboru input_15.txt"""
    with open(filename, 'r') as f:
        content = f.read()
    # Vyfiltruje pouze platné pohybové příkazy
    return ''.join(c for c in content if c in '<>^v')

def load_map_file(filename: str) -> List[str]:
    """Načte mapu ze souboru warehouse_map.txt"""
    with open(filename, 'r') as f:
        return [line.rstrip() for line in f.readlines()]

class Box:
    def __init__(self, x: int, y: int):
        self.x = x  # Levá pozice boxu
        self.y = y
        self.width = 2

    def get_positions(self) -> Set[Tuple[int, int]]:
        return {(self.x, self.y), (self.x + 1, self.y)}

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def get_gps(self) -> int:
        # GPS = 100 * y + x, kde y a x jsou vzdálenosti od horního a levého okraje
        # Počítáme pro levou stranu krabice (self.x)
        # y začíná od 0, x začíná od 0
        gps = 100 * self.y + self.x
        return gps

class WarehouseGame:
    def __init__(self):
        # Načtení mapy a pohybů ze správných souborů
        self.map_lines = load_map_file("Day_15/warehouse_map.txt")
        self.moves = load_moves_sequence("Day_15/input_15.txt")
        
        self.load_map()
        self.move_index = 0
        self.auto_play = False
        self.move_delay = 0.1
        self.last_move_time = 0
        
        pygame.init()
        
        # Získání rozlišení obrazovky
        screen_info = pygame.display.Info()
        self.screen_width = int(screen_info.current_w * 0.8)  # 80% obrazovky
        self.screen_height = int(screen_info.current_h * 0.8)
        
        # Nastavení velikosti buňky
        self.cell_size = 30  # Fixní velikost buňky pro čitelnost
        
        # Vytvoření hlavního okna
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Warehouse Robot - Part Two")
        
        # Vytvoření surface pro celou mapu
        self.map_width = len(self.map[0]) * self.cell_size
        self.map_height = len(self.map) * self.cell_size
        self.map_surface = pygame.Surface((self.map_width, self.map_height))
        
        # Viewport pozice (pro scrollování)
        self.viewport_x = 0
        self.viewport_y = 0
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, min(self.cell_size, 24))  # Menší font pro čísla
        
        # Barvy
        self.WALL_COLOR = (100, 100, 100)
        self.BOX_COLOR = (160, 82, 45)
        self.ROBOT_COLOR = (255, 0, 0)
        self.BACKGROUND_COLOR = (240, 240, 240)

    def load_map(self):
        """Načte mapu a inicializuje pozice robota a krabic"""
        self.map = []
        self.boxes = []
        
        for y, line in enumerate(self.map_lines):
            row = list(line)  # Pro snadnější manipulaci s mapou
            for x in range(len(row) - 1):
                if row[x:x+2] == ['[', ']']:
                    self.boxes.append(Box(x, y))
                elif row[x:x+2] == ['@', '.']:
                    self.robot_x = x
                    self.robot_y = y
            self.map.append(row)

    def find_connected_boxes(self, start_box: Box, dx: int, dy: int) -> Set[Box]:
        """Najde všechny propojené krabice ve směru pohybu"""
        connected = {start_box}
        to_check = [start_box]
        
        while to_check:
            current_box = to_check.pop()
            current_positions = current_box.get_positions()
            
            for box in self.boxes:
                if box not in connected:
                    box_positions = box.get_positions()
                    
                    # Kontrolujeme propojení pouze ve směru pohybu
                    if dx != 0:  # Horizontální pohyb
                        # Kontrola jen horizontálního propojení
                        if box.y == current_box.y:  # Musí být ve stejné řadě
                            if dx > 0:  # Pohyb doprava
                                if any(pos[0] + 1 == box.x for pos in current_positions):
                                    connected.add(box)
                                    to_check.append(box)
                            else:  # Pohyb doleva
                                if any(pos[0] - 1 == box.x + 1 for pos in current_positions):
                                    connected.add(box)
                                    to_check.append(box)
                    
                    elif dy != 0:  # Vertikální pohyb
                        # Pro vertikální pohyb kontrolujeme překryv v x-ové souřadnici
                        box_x_positions = {x for x, _ in box_positions}
                        current_x_positions = {x for x, _ in current_positions}
                        
                        if box_x_positions & current_x_positions:  # Existuje překryv v x-ové souřadnici
                            if dy > 0:  # Pohyb dolů
                                if any(pos[1] + 1 == box.y for pos in current_positions):
                                    connected.add(box)
                                    to_check.append(box)
                            else:  # Pohyb nahoru
                                if any(pos[1] - 1 == box.y + 1 for pos in current_positions):
                                    connected.add(box)
                                    to_check.append(box)
        
        return connected

    def find_pushed_boxes(self, new_x: int, new_y: int, dx: int, dy: int) -> Set[Box]:
        """Najde všechny krabice, které by měly být posunuty při pohybu robota"""
        directly_pushed = set()
        
        # Nejdřív najdi krabice, které robot přímo tlačí
        for box in self.boxes:
            if (new_x, new_y) in box.get_positions():
                directly_pushed.add(box)

        if not directly_pushed:
            return set()

        # Pro každou přímo tlačenou krabici najdi propojené krabice ve směru pohybu
        all_pushed = set()
        for start_box in directly_pushed:
            to_check = [start_box]
            checked = {start_box}
            
            while to_check:
                current_box = to_check.pop()
                all_pushed.add(current_box)
                
                # Pozice aktuální krabice
                current_positions = current_box.get_positions()
                
                # Hledej další krabice ve směru pohybu
                for box in self.boxes:
                    if box not in checked:
                        box_positions = box.get_positions()
                        
                        # Pro vertikální pohyb
                        if dy != 0:
                            # Musí být aspoň částečné překrytí v x-ové souřadnici
                            box_x_range = range(box.x, box.x + 2)
                            current_x_range = range(current_box.x, current_box.x + 2)
                            if any(x in box_x_range for x in current_x_range):
                                if dy > 0 and box.y == current_box.y + 1:  # Pohyb dolů
                                    checked.add(box)
                                    to_check.append(box)
                                elif dy < 0 and box.y == current_box.y - 1:  # Pohyb nahoru
                                    checked.add(box)
                                    to_check.append(box)
                        
                        # Pro horizontální pohyb
                        if dx != 0:
                            if box.y == current_box.y:  # Musí být ve stejné řadě
                                if dx > 0 and box.x == current_box.x + 2:  # Pohyb doprava
                                    checked.add(box)
                                    to_check.append(box)
                                elif dx < 0 and box.x == current_box.x - 2:  # Pohyb doleva
                                    checked.add(box)
                                    to_check.append(box)
        
        return all_pushed

    def can_move_boxes(self, boxes: Set[Box], dx: int, dy: int) -> bool:
        """Kontroluje, zda je možné posunout skupinu krabic"""
        # Kontrola pro každou krabici v množině
        for box in boxes:
            new_x = box.x + dx
            new_y = box.y + dy
            
            # Kontrola kolize se zdí
            if not (0 <= new_x < len(self.map[0]) - 1 and 0 <= new_y < len(self.map)):
                return False
            if self.map[new_y][new_x] == '#' or self.map[new_y][new_x + 1] == '#':
                return False
            
            # Kontrola kolize s ostatními krabicemi
            new_positions = {(new_x, new_y), (new_x + 1, new_y)}
            for other_box in self.boxes:
                if other_box not in boxes:  # Nekontrolujeme kolize s krabicemi, které také posouváme
                    if any(pos in new_positions for pos in other_box.get_positions()):
                        return False
        
        return True

    def move_robot(self, dx: int, dy: int) -> bool:
        """Pohyb robota a případný posun krabic"""
        new_x = self.robot_x + dx
        new_y = self.robot_y + dy
        
        # Kontrola kolize se zdí
        if not (0 <= new_x < len(self.map[0]) and 0 <= new_y < len(self.map)):
            return False
        if self.map[new_y][new_x] == '#':
            return False
        
        # Najdi krabice, které budou posunuty
        pushed_boxes = self.find_pushed_boxes(new_x, new_y, dx, dy)
        
        # Pokud jsou nějaké krabice k posunutí, zkontroluj, zda je můžeme posunout
        if pushed_boxes and not self.can_move_boxes(pushed_boxes, dx, dy):
            return False
        
        # Posun krabic
        for box in pushed_boxes:
            box.move(dx, dy)
        
        # Posun robota
        self.robot_x = new_x
        self.robot_y = new_y
        return True

    def process_move(self, move: str) -> bool:
        if move == '^':
            return self.move_robot(0, -1)
        elif move == 'v':
            return self.move_robot(0, 1)
        elif move == '<':
            return self.move_robot(-1, 0)
        elif move == '>':
            return self.move_robot(1, 0)
        return False

    def update_viewport(self):
        """Aktualizuje viewport tak, aby byl robot viditelný"""
        margin = self.cell_size * 5  # Margin kolem robota
        
        # Výpočet cílové pozice viewportu
        target_x = self.robot_x * self.cell_size - self.screen_width // 2
        target_y = self.robot_y * self.cell_size - self.screen_height // 2
        
        # Omezení viewportu na hranice mapy
        self.viewport_x = max(0, min(target_x, self.map_width - self.screen_width))
        self.viewport_y = max(0, min(target_y, self.map_height - self.screen_height))

    def draw(self):
        # Vyčištění obou povrchů
        self.map_surface.fill(self.BACKGROUND_COLOR)
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Vykreslení zdí
        for y, row in enumerate(self.map):
            for x in range(0, len(row), 2):
                if ''.join(row[x:x+2]) == '##':
                    pygame.draw.rect(self.map_surface, self.WALL_COLOR,
                                  (x * self.cell_size, y * self.cell_size,
                                   self.cell_size * 2, self.cell_size))
        
        # Vykreslení boxů s GPS souřadnicemi
        for box in self.boxes:
            # Vykreslení boxu
            pygame.draw.rect(self.map_surface, self.BOX_COLOR,
                          (box.x * self.cell_size, box.y * self.cell_size,
                           self.cell_size * 2, self.cell_size))
            pygame.draw.rect(self.map_surface, (0, 0, 0),
                          (box.x * self.cell_size, box.y * self.cell_size,
                           self.cell_size * 2, self.cell_size), 1)
            
            # Vykreslení GPS souřadnice na boxu
            gps = box.get_gps()
            gps_text = self.font.render(str(gps), True, (255, 255, 255))
            text_rect = gps_text.get_rect()
            text_rect.center = (
                box.x * self.cell_size + self.cell_size,
                box.y * self.cell_size + self.cell_size // 2
            )
            # Tmavé pozadí pro text
            pygame.draw.rect(self.map_surface, (0, 0, 0),
                           (text_rect.x - 1, text_rect.y - 1,
                            text_rect.width + 2, text_rect.height + 2))
            self.map_surface.blit(gps_text, text_rect)
        
        # Vykreslení robota
        pygame.draw.rect(self.map_surface, self.ROBOT_COLOR,
                      (self.robot_x * self.cell_size, self.robot_y * self.cell_size,
                       self.cell_size, self.cell_size))
        pygame.draw.rect(self.map_surface, (0, 0, 0),
                      (self.robot_x * self.cell_size, self.robot_y * self.cell_size,
                       self.cell_size, self.cell_size), 1)
        
        # Aktualizace viewportu pro sledování robota
        self.update_viewport()
        
        # Vykreslení viditelné části mapy
        self.screen.blit(self.map_surface, 
                        (0, 0), 
                        (self.viewport_x, self.viewport_y, 
                         self.screen_width, self.screen_height))
        
        # Vykreslení informací
        moves_left = len(self.moves) - self.move_index
        status = f"Zbývá tahů: {moves_left} | SPACE: start/stop, R: reset, +/-: rychlost"
        text = self.font.render(status, True, (0, 0, 0))
        self.screen.blit(text, (10, self.screen_height - 30))
        
        pygame.display.flip()

    def reset(self):
        """Reset hry do počátečního stavu"""
        self.load_map()
        self.move_index = 0
        self.auto_play = False

    def run(self):
        running = True
        while running:
            current_time = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.auto_play = not self.auto_play
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        self.move_delay = max(0.01, self.move_delay - 0.05)
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        self.move_delay += 0.05
                    # Manuální scrollování pro testování
                    elif event.key == pygame.K_LEFT:
                        self.viewport_x = max(0, self.viewport_x - self.cell_size)
                    elif event.key == pygame.K_RIGHT:
                        self.viewport_x = min(self.map_width - self.screen_width, 
                                           self.viewport_x + self.cell_size)
                    elif event.key == pygame.K_UP:
                        self.viewport_y = max(0, self.viewport_y - self.cell_size)
                    elif event.key == pygame.K_DOWN:
                        self.viewport_y = min(self.map_height - self.screen_height,
                                           self.viewport_y + self.cell_size)
            
            if self.auto_play and self.move_index < len(self.moves):
                if current_time - self.last_move_time >= self.move_delay:
                    self.process_move(self.moves[self.move_index])
                    self.move_index += 1
                    self.last_move_time = current_time
                    
                    if self.move_index >= len(self.moves):
                        self.auto_play = False
                        total_gps = sum(box.get_gps() for box in self.boxes)
                        print(f"Součet GPS souřadnic: {total_gps}")
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = WarehouseGame()
    game.run()