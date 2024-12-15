import pygame
import sys
from dataclasses import dataclass
from typing import List

WIDTH = 101
HEIGHT = 103
SCALE = 8
WINDOW_WIDTH = WIDTH * SCALE
WINDOW_HEIGHT = HEIGHT * SCALE
FPS = 10

@dataclass
class Robot:
    x: float  
    y: float
    vx: int
    vy: int

def parse_input(filename: str) -> List[Robot]:
    robots = []
    with open(filename, 'r') as f:
        for line in f:
            pos, vel = line.strip().split()
            x, y = map(int, pos[2:].split(','))
            vx, vy = map(int, vel[2:].split(','))
            robots.append(Robot(float(x), float(y), vx, vy))
    return robots

def simulate_step(robots: List[Robot]):
    for robot in robots:
        robot.x = (robot.x + robot.vx) % WIDTH
        robot.y = (robot.y + robot.vy) % HEIGHT

class Visualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Robot Movement Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.robots = parse_input("Day_14/input_14.txt")
        self.time = 0
        self.paused = True
        self.speed = 1.0

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
                    self.robots = parse_input("Day_14/input_14.txt")
                    self.time = 0
                elif event.key == pygame.K_UP:
                    self.speed = min(5.0, self.speed + 0.1)
                elif event.key == pygame.K_DOWN:
                    self.speed = max(0.1, self.speed - 0.1)
        return True

    def step(self):
        simulate_step(self.robots)
        self.time += 1

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        for robot in self.robots:
            x = int(robot.x * SCALE)
            y = int(robot.y * SCALE)
            pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 2)
        
        # Informační panel
        info_text = f"Čas: {self.time}s  Rychlost: {self.speed:.1f}x  {'PAUZA' if self.paused else 'BĚŽÍ'}"
        text_surface = self.font.render(info_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))
        
        pygame.display.flip()

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