import pygame
import sys
from dataclasses import dataclass
from typing import List, Set, Tuple
from collections import defaultdict

# Konstanty
WIDTH = 101
HEIGHT = 103
SCALE = 8  # Velikost pixelů pro každou buňku
WINDOW_WIDTH = WIDTH * SCALE
WINDOW_HEIGHT = HEIGHT * SCALE + 100  # Extra prostor pro ovládací panel
FPS = 60

@dataclass
class Robot:
    x: float
    y: float
    vx: int
    vy: int

class Visualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Robot Pattern Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.robots = self.parse_input("Day_14/input_14.txt")
        self.time = 0
        self.paused = True
        self.speed = 1.0
        self.show_heatmap = False
        self.trail_length = 10
        self.trails = []  # Historie pozic pro každého robota

    def parse_input(self, filename: str) -> List[Robot]:
        robots = []
        with open(filename, 'r') as f:
            for line in f:
                pos, vel = line.strip().split()
                x, y = map(int, pos[2:].split(','))
                vx, vy = map(int, vel[2:].split(','))
                robots.append(Robot(float(x), float(y), vx, vy))
        return robots

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_RIGHT and self.paused:
                    self.step()
                elif event.key == pygame.K_r:  # Reset
                    self.robots = self.parse_input("Day_14/input_14.txt")
                    self.time = 0
                    self.trails = []
                elif event.key == pygame.K_h:  # Toggle heatmap
                    self.show_heatmap = not self.show_heatmap
                elif event.key == pygame.K_UP:
                    self.speed = min(5.0, self.speed + 0.1)
                elif event.key == pygame.K_DOWN:
                    self.speed = max(0.1, self.speed - 0.1)
                elif event.key == pygame.K_s:  # Save interesting positions
                    self.save_positions()
        return True

    def step(self):
        # Aktualizace pozic
        current_positions = []
        for robot in self.robots:
            robot.x = (robot.x + robot.vx) % WIDTH
            robot.y = (robot.y + robot.vy) % HEIGHT
            current_positions.append((int(robot.x), int(robot.y)))
        
        # Aktualizace trails
        self.trails.append(current_positions)
        if len(self.trails) > self.trail_length:
            self.trails.pop(0)
        
        self.time += 1

    def draw_heatmap(self):
        # Vytvoření heatmapy z aktuálních pozic
        heatmap = defaultdict(int)
        for robot in self.robots:
            x, y = int(robot.x), int(robot.y)
            heatmap[(x, y)] += 1
        
        # Vykreslení heatmapy
        max_heat = max(heatmap.values())
        for (x, y), heat in heatmap.items():
            intensity = int(255 * heat / max_heat)
            color = (0, 0, intensity)
            pygame.draw.rect(self.screen, color,
                           (x * SCALE, y * SCALE, SCALE, SCALE))

    def draw(self):
        self.screen.fill((255, 255, 255))  # Bílé pozadí
        
        # Vykreslení heatmapy nebo robotů
        if self.show_heatmap:
            self.draw_heatmap()
        else:
            # Vykreslení trails
            for i, trail in enumerate(self.trails):
                alpha = int(255 * (i + 1) / len(self.trails))
                for x, y in trail:
                    pygame.draw.circle(self.screen, 
                                    (0, 0, 255, alpha),
                                    (int(x * SCALE), int(y * SCALE)), 
                                    2)
            
            # Vykreslení aktuálních pozic robotů
            for robot in self.robots:
                x = int(robot.x * SCALE)
                y = int(robot.y * SCALE)
                pygame.draw.circle(self.screen, (0, 0, 255), (x, y), 3)
        
        # Informační panel
        info_text = [
            f"Čas: {self.time}s",
            f"Rychlost: {self.speed:.1f}x",
            f"{'PAUZA' if self.paused else 'BĚŽÍ'}",
            f"{'Heatmapa' if self.show_heatmap else 'Normální'}"
        ]
        y_offset = WINDOW_HEIGHT - 90
        for text in info_text:
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 30
        
        pygame.display.flip()

    def save_positions(self):
        """Uloží aktuální pozice do souboru"""
        with open(f"positions_time_{self.time}.txt", "w") as f:
            for robot in self.robots:
                f.write(f"{int(robot.x)},{int(robot.y)}\n")
        print(f"Pozice uloženy v čase {self.time}")

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            if not self.paused:
                for _ in range(int(self.speed)):
                    self.step()
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    viz = Visualizer()
    viz.run()

if __name__ == "__main__":
    main()