import pygame
import sys
import time
from copy import deepcopy

class ScrollBar:
    def __init__(self, x, y, length, is_horizontal=True, max_scroll=0):
        self.is_horizontal = is_horizontal
        if is_horizontal:
            self.rect = pygame.Rect(x, y, length, 15)
        else:
            self.rect = pygame.Rect(x, y, 15, length)
        self.max_scroll = max_scroll
        self.scroll_pos = 0
        self.is_dragging = False
        self.slider_size = 50  # minimální velikost posuvníku

    def draw(self, screen):
        # Pozadí scrollbaru
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 1)

        # Výpočet velikosti a pozice posuvníku
        if self.max_scroll > 0:
            if self.is_horizontal:
                slider_x = self.rect.x + (self.scroll_pos / self.max_scroll) * (self.rect.width - self.slider_size)
                slider_rect = pygame.Rect(slider_x, self.rect.y, self.slider_size, self.rect.height)
            else:
                slider_y = self.rect.y + (self.scroll_pos / self.max_scroll) * (self.rect.height - self.slider_size)
                slider_rect = pygame.Rect(self.rect.x, slider_y, self.rect.width, self.slider_size)
            
            pygame.draw.rect(screen, (150, 150, 150), slider_rect)
            pygame.draw.rect(screen, (100, 100, 100), slider_rect, 1)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                return self.update_scroll(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            return self.update_scroll(event.pos)
        
        return False

    def update_scroll(self, pos):
        if self.is_horizontal:
            rel_x = (pos[0] - self.rect.x) / self.rect.width
            self.scroll_pos = max(0, min(self.max_scroll, rel_x * self.max_scroll))
        else:
            rel_y = (pos[1] - self.rect.y) / self.rect.height
            self.scroll_pos = max(0, min(self.max_scroll, rel_y * self.max_scroll))
        return True

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.default_text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_toggled = False

    def draw(self, screen):
        # Převedení generátoru na tuple pro barvy
        color = self.hover_color if self.is_hovered else self.color
        if self.is_toggled:
            color = tuple(max(0, c - 50) for c in color)
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

    def toggle(self, state=None):
        if state is None:
            self.is_toggled = not self.is_toggled
        else:
            self.is_toggled = state
        self.text = 'Stop' if self.is_toggled else self.default_text

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.is_held = False
        
    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        # Vypočítej pozici posuvníku
        slider_pos = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        slider_rect = pygame.Rect(slider_pos - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(screen, (100, 100, 100), slider_rect)
        
        # Vykresli hodnotu
        font = pygame.font.Font(None, 24)
        text = font.render(f"{self.value:.1f}", True, (0, 0, 0))
        text_rect = text.get_rect(midtop=(self.rect.centerx, self.rect.bottom + 5))
        screen.blit(text, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_held = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_held = False
        elif event.type == pygame.MOUSEMOTION and self.is_held:
            rel_x = min(max(event.pos[0], self.rect.left), self.rect.right)
            self.value = self.min_val + (rel_x - self.rect.left) / self.rect.width * (self.max_val - self.min_val)
            return True
        return False

class WarehouseSimulation:
    def __init__(self, width=1200, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.cell_size = 40
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Warehouse Robot Simulation")
        
        # Scrolling
        self.scroll_x = 0
        self.scroll_y = 0
        self.max_scroll_x = 0
        self.max_scroll_y = 0
        
        # Scrollbary
        self.h_scrollbar = None  # Bude inicializováno po načtení mapy
        self.v_scrollbar = None  # Bude inicializováno po načtení mapy
        
        # GUI prvky
        self.buttons = {
            'up': Button(width - 150, 50, 50, 50, '↑', (200, 200, 200), (150, 150, 150)),
            'down': Button(width - 150, 150, 50, 50, '↓', (200, 200, 200), (150, 150, 150)),
            'left': Button(width - 200, 100, 50, 50, '←', (200, 200, 200), (150, 150, 150)),
            'right': Button(width - 100, 100, 50, 50, '→', (200, 200, 200), (150, 150, 150)),
            'play': Button(width - 150, 250, 100, 50, 'Play', (150, 255, 150), (100, 200, 100)),
            'reset': Button(width - 150, 320, 100, 50, 'Reset', (255, 150, 150), (200, 100, 100))
        }
        
        # Slider pro rychlost
        self.speed_slider = Slider(width - 200, 400, 150, 20, 10.0, 1000.0, 50.0)
        
        # Barvy
        self.COLORS = {
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255),
            'GRAY': (128, 128, 128),
            'RED': (255, 0, 0),
            'BROWN': (139, 69, 19),
            'GREEN': (0, 255, 0)
        }
        
        # Stav hry
        self.initial_map = []
        self.initial_robot_pos = None
        self.map_data = []
        self.robot_pos = None
        self.moves = ""
        self.move_index = 0
        self.auto_play = False
        self.move_delay = 0.01
        self.last_move_time = 0

    def load_map(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read().strip().split('\n')
                
            map_start = None
            map_end = None
            
            for i, line in enumerate(content):
                if '#' in line:
                    if map_start is None:
                        map_start = i
                    map_end = i
                elif map_start is not None and not line.strip():
                    break
            
            # Načti mapu včetně všech zdí
            if map_start is not None and map_end is not None:
                self.map_data = [list(line) for line in content[map_start:map_end + 1]]
                self.initial_map = deepcopy(self.map_data)
            
                # Najdi pozici robota
                for y, row in enumerate(self.map_data):
                    for x, cell in enumerate(row):
                        if cell == '@':
                            self.robot_pos = (x, y)
                            self.initial_robot_pos = (x, y)
            
                # Nastav maximální scrollování
                map_width = len(self.map_data[0]) * self.cell_size
                map_height = len(self.map_data) * self.cell_size
                self.max_scroll_x = max(0, map_width - (self.width - 300))
                self.max_scroll_y = max(0, map_height - self.height)
                
                # Načti pohyby (spojí všechny řádky po mapě)
                moves_content = content[map_end + 2:]  # Skip prázdný řádek
                self.moves = ''.join(
                    char for line in moves_content 
                    for char in line.strip() 
                    if char in '^v<>'
                )
            else:
                raise ValueError("Nepodařilo se najít mapu v souboru")
            
        except Exception as e:
            print(f"Chyba při načítání souboru: {e}")
            sys.exit(1)

    def reset(self):
        self.map_data = deepcopy(self.initial_map)
        self.robot_pos = self.initial_robot_pos
        self.move_index = 0
        self.auto_play = False
        self.scroll_x = 0
        self.scroll_y = 0
    
    def calculate_gps(self):
        total_gps = 0
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == 'O':
                    gps = 100 * y + x
                    total_gps += gps
        return total_gps
    
    def can_push_boxes(self, x, y, dx, dy):
        current_x, current_y = x, y
        boxes = []
        
        while self.map_data[current_y][current_x] == 'O':
            boxes.append((current_x, current_y))
            current_x += dx
            current_y += dy
            if not (0 <= current_x < len(self.map_data[0]) and 0 <= current_y < len(self.map_data)):
                return False
            if self.map_data[current_y][current_x] == '#':
                return False
                
        if self.map_data[current_y][current_x] == '.':
            return boxes
        return False
    
    def move_robot(self, dx, dy):
        new_x = self.robot_pos[0] + dx
        new_y = self.robot_pos[1] + dy
        
        if not (0 <= new_x < len(self.map_data[0]) and 0 <= new_y < len(self.map_data)):
            return False
            
        if self.map_data[new_y][new_x] == '#':
            return False
        
        if self.map_data[new_y][new_x] == '.':
            self.map_data[self.robot_pos[1]][self.robot_pos[0]] = '.'
            self.map_data[new_y][new_x] = '@'
            self.robot_pos = (new_x, new_y)
            return True
            
        elif self.map_data[new_y][new_x] == 'O':
            boxes = self.can_push_boxes(new_x, new_y, dx, dy)
            if boxes:
                for box_x, box_y in reversed(boxes):
                    self.map_data[box_y + dy][box_x + dx] = 'O'
                    self.map_data[box_y][box_x] = '.'
                
                self.map_data[self.robot_pos[1]][self.robot_pos[0]] = '.'
                self.map_data[new_y][new_x] = '@'
                self.robot_pos = (new_x, new_y)
                return True
                
        return False
    
    def process_move(self, move):
        if move == '^':
            return self.move_robot(0, -1)
        elif move == 'v':
            return self.move_robot(0, 1)
        elif move == '<':
            return self.move_robot(-1, 0)
        elif move == '>':
            return self.move_robot(1, 0)
        return False
    
    def draw(self):
        self.screen.fill(self.COLORS['WHITE'])
        
        # Vykresli mapu s posunutím
        visible_area = pygame.Rect(self.scroll_x, self.scroll_y, self.width - 300, self.height)
        
        if self.h_scrollbar:
            self.h_scrollbar.draw(self.screen)
        if self.v_scrollbar:
            self.v_scrollbar.draw(self.screen)
        
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                screen_x = x * self.cell_size - self.scroll_x
                screen_y = y * self.cell_size - self.scroll_y
                
                if not (0 <= screen_x < self.width - 300 and 0 <= screen_y < self.height):
                    continue
                    
                rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)
                
                if cell == '#':
                    pygame.draw.rect(self.screen, self.COLORS['GRAY'], rect)
                elif cell == 'O':
                    pygame.draw.rect(self.screen, self.COLORS['BROWN'], rect)
                    gps = str(100 * y + x)
                    font = pygame.font.Font(None, 20)
                    text = font.render(gps, True, self.COLORS['WHITE'])
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
                elif cell == '@':
                    pygame.draw.rect(self.screen, self.COLORS['RED'], rect)
                    
                pygame.draw.rect(self.screen, self.COLORS['BLACK'], rect, 1)
        
        # GUI
        pygame.draw.rect(self.screen, (240, 240, 240), (self.width - 300, 0, 300, self.height))
        
        font = pygame.font.Font(None, 36)
        gps_text = font.render(f"Total GPS: {self.calculate_gps()}", True, self.COLORS['BLACK'])
        self.screen.blit(gps_text, (self.width - 280, 10))
        
        mode_text = font.render(f"Speed: {self.speed_slider.value:.1f}x", True, self.COLORS['BLACK'])
        self.screen.blit(mode_text, (self.width - 280, 370))
        
        if self.move_index < len(self.moves):
            next_moves = self.moves[self.move_index:self.move_index + 20]
            moves_text = font.render(f"Next: {next_moves}", True, self.COLORS['BLACK'])
            self.screen.blit(moves_text, (10, 10))
        
        progress_text = font.render(f"Move: {self.move_index}/{len(self.moves)}", True, self.COLORS['BLACK'])
        self.screen.blit(progress_text, (self.width - 280, 450))
        
        # Vykresli tlačítka a slider
        for button in self.buttons.values():
            button.draw(self.screen)
        self.speed_slider.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        dragging = False
        last_mouse_pos = None
        
        while True:
            current_time = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                # Ovládání slideru
                if self.speed_slider.handle_event(event):
                    self.move_delay = 0.01 / self.speed_slider.value
                
                # Ovládání tlačítek
                for name, button in self.buttons.items():
                    if button.handle_event(event):
                        if name == 'play':
                            self.auto_play = not self.auto_play
                            button.toggle()
                            self.last_move_time = current_time  # Reset časovače
                        elif name == 'reset':
                            self.reset()
                            self.buttons['play'].toggle(False)
                            self.auto_play = False
                        elif not self.auto_play:
                            if name == 'up':
                                self.process_move('^')
                            elif name == 'down':
                                self.process_move('v')
                            elif name == 'left':
                                self.process_move('<')
                            elif name == 'right':
                                self.process_move('>')
                
                # Kontrola událostí scrollbarů
                if self.h_scrollbar and self.h_scrollbar.handle_event(event):
                    self.scroll_x = self.h_scrollbar.scroll_pos
                if self.v_scrollbar and self.v_scrollbar.handle_event(event):
                    self.scroll_y = self.v_scrollbar.scroll_pos
                
                # Scrollování myší
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos[0] < self.width - 300:  # Pouze v oblasti mapy
                            dragging = True
                            last_mouse_pos = event.pos
                            
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False
                        
                elif event.type == pygame.MOUSEMOTION:
                    if dragging and last_mouse_pos:
                        dx = last_mouse_pos[0] - event.pos[0]
                        dy = last_mouse_pos[1] - event.pos[1]
                        
                        self.scroll_x = max(0, min(self.max_scroll_x, self.scroll_x + dx))
                        self.scroll_y = max(0, min(self.max_scroll_y, self.scroll_y + dy))
                        
                        last_mouse_pos = event.pos
                
                # Klávesové ovládání
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.auto_play = not self.auto_play
                        self.buttons['play'].toggle()
                    elif event.key == pygame.K_r:
                        self.reset()
                        self.buttons['play'].toggle(False)
                        self.auto_play = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif not self.auto_play:
                        if event.key == pygame.K_UP:
                            self.process_move('^')
                        elif event.key == pygame.K_DOWN:
                            self.process_move('v')
                        elif event.key == pygame.K_LEFT:
                            self.process_move('<')
                        elif event.key == pygame.K_RIGHT:
                            self.process_move('>')
            
            # Aktualizace pozice scrollbarů při scrollování myší
            if self.h_scrollbar:
                self.h_scrollbar.scroll_pos = self.scroll_x
            if self.v_scrollbar:
                self.v_scrollbar.scroll_pos = self.scroll_y

            # Auto-play logika
            if self.auto_play and self.move_index < len(self.moves):
                current_time = time.time()
                if current_time - self.last_move_time >= self.move_delay:
                    current_move = self.moves[self.move_index]
                    # Bez ohledu na výsledek pohybu přejdeme na další příkaz
                    self.process_move(current_move)
                    self.move_index += 1
                    
                    if self.move_index >= len(self.moves):
                        self.auto_play = False
                        self.buttons['play'].toggle(False)
                    self.last_move_time = current_time

                    # Automatické scrollování k robotovi
                    robot_screen_x = self.robot_pos[0] * self.cell_size - self.scroll_x
                    robot_screen_y = self.robot_pos[1] * self.cell_size - self.scroll_y
                    
                    margin = 100  # Okraj pro scrollování
                    if robot_screen_x < margin:
                        self.scroll_x = max(0, self.robot_pos[0] * self.cell_size - margin)
                    elif robot_screen_x > self.width - 300 - margin:
                        self.scroll_x = min(self.max_scroll_x, self.robot_pos[0] * self.cell_size - (self.width - 300 - margin))
                    
                    if robot_screen_y < margin:
                        self.scroll_y = max(0, self.robot_pos[1] * self.cell_size - margin)
                    elif robot_screen_y > self.height - margin:
                        self.scroll_y = min(self.max_scroll_y, self.robot_pos[1] * self.cell_size - (self.height - margin))
            
            self.draw()
            clock.tick(60)

if __name__ == "__main__":
    game = WarehouseSimulation()
    game.load_map("Day_15/input_15.txt")
    game.run()