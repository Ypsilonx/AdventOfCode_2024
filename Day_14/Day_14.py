from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

def read_input(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read().strip()

def parse_input(input_text: str) -> List[Robot]:
    robots = []
    for line in input_text.strip().split('\n'):
        pos, vel = line.split()
        x, y = map(int, pos[2:].split(','))
        vx, vy = map(int, vel[2:].split(','))
        robots.append(Robot(x, y, vx, vy))
    return robots

def simulate_step(robots: List[Robot], width: int, height: int):
    for robot in robots:
        robot.x = (robot.x + robot.vx) % width
        robot.y = (robot.y + robot.vy) % height

def count_robots_in_quadrants(robots: List[Robot], width: int, height: int) -> Tuple[int, int, int, int]:
    mid_x = width // 2
    mid_y = height // 2
    
    quadrants = [0] * 4
    
    for robot in robots:
        if robot.x == mid_x or robot.y == mid_y:
            continue
            
        quad_x = 1 if robot.x > mid_x else 0
        quad_y = 1 if robot.y > mid_y else 0
        quadrant = quad_y * 2 + quad_x
        quadrants[quadrant] += 1
    
    return tuple(quadrants)

def solve(input_text: str, width: int = 101, height: int = 103, steps: int = 100) -> int:
    robots = parse_input(input_text)
    
    for _ in range(steps):
        simulate_step(robots, width, height)
    
    q1, q2, q3, q4 = count_robots_in_quadrants(robots, width, height)
    return q1 * q2 * q3 * q4

input_data = read_input("Day_14/input_14.txt")
result = solve(input_data)
print(f"Safety factor for actual input: {result}")

example_input = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip()

example_result = solve(example_input, width=11, height=7)
print(f"Example safety factor: {example_result}")  # Should print 12