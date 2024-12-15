from dataclasses import dataclass
from typing import List, Tuple
import math
from collections import defaultdict

@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Rozšířený Euklidův algoritmus.
    Vrací (gcd, x, y) kde gcd je největší společný dělitel a
    x, y jsou koeficienty Bézoutovy identity: ax + by = gcd
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a: int, m: int) -> int:
    """Nalezne modulární multiplikativní inverzi a modulo m"""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Modulární inverze neexistuje ({a} mod {m})")
    return (x % m + m) % m

def chinese_remainder(remainders: List[int], moduli: List[int]) -> int:
    """
    Implementace Chinese Remainder Theorem.
    Řeší systém kongruencí:
    x ≡ remainders[i] (mod moduli[i])
    """
    total = 0
    product = math.lcm(*moduli)
    
    for remainder, modulus in zip(remainders, moduli):
        p = product // modulus
        total += remainder * p * mod_inverse(p, modulus)
    
    return total % product

def find_robot_period(robot: Robot, width: int, height: int) -> Tuple[int, int, int]:
    """
    Najde periodu pohybu robota a jeho pozici v této periodě.
    Vrací (perioda_x, perioda_y, celková_perioda)
    """
    # Perioda v x-ové souřadnici
    if robot.vx == 0:
        period_x = 1
    else:
        period_x = width // math.gcd(abs(robot.vx), width)
    
    # Perioda v y-ové souřadnici
    if robot.vy == 0:
        period_y = 1
    else:
        period_y = height // math.gcd(abs(robot.vy), height)
    
    # Celková perioda je nejmenší společný násobek period
    total_period = math.lcm(period_x, period_y)
    
    return period_x, period_y, total_period

def find_pattern_time(robots: List[Robot], width: int = 101, height: int = 103) -> int:
    """
    Pokusí se najít čas, kdy se roboti uspořádají do vzoru.
    """
    # Analyzujeme periody všech robotů
    robot_periods = [find_robot_period(robot, width, height) for robot in robots]
    
    # Pro každého robota vypočítáme jeho pozice v čase
    position_times = defaultdict(list)
    for i, robot in enumerate(robots):
        period = robot_periods[i][2]
        for t in range(period):
            x = (robot.x + robot.vx * t) % width
            y = (robot.y + robot.vy * t) % height
            position_times[(x, y)].append((i, t, period))
    
    # Hledáme pozice, kde se setkává více robotů
    interesting_positions = {pos: times for pos, times in position_times.items() 
                           if len(times) > 1}
    
    print(f"Nalezeno {len(interesting_positions)} zajímavých pozic")
    
    # Pokusíme se najít řešení pomocí CRT pro každou skupinu robotů
    for pos, times in interesting_positions.items():
        if len(times) >= len(robots) * 0.1:  # Aspoň 10% robotů
            print(f"\nAnalyzuji pozici {pos} s {len(times)} roboty")
            remainders = [t for _, t, _ in times]
            moduli = [p for _, _, p in times]
            
            try:
                solution = chinese_remainder(remainders, moduli)
                print(f"Možné řešení v čase: {solution}")
                # Ověříme řešení
                all_positions = get_positions_at_time(robots, solution, width, height)
                if is_interesting_pattern(all_positions):
                    return solution
            except ValueError as e:
                print(f"Nelze najít řešení pro tuto skupinu: {e}")
    
    return -1

def get_positions_at_time(robots: List[Robot], time: int, width: int, height: int) -> List[Tuple[int, int]]:
    """Získá pozice všech robotů v daném čase"""
    positions = []
    for robot in robots:
        # Vypočítáme novou pozici pro každého robota
        new_x = (robot.x + robot.vx * time) % width
        new_y = (robot.y + robot.vy * time) % height
        positions.append([new_x, new_y])
    return positions

def is_interesting_pattern(positions: List[Tuple[int, int]]) -> bool:
    """
    Zkontroluje, zda pozice tvoří zajímavý vzor.
    Tuto funkci můžete upravit podle toho, jaký vzor hledáte.
    """
    # Počítáme hustotu robotů v různých částech
    grid = defaultdict(int)
    for x, y in positions:
        grid[x//10, y//10] += 1
    
    # Hledáme oblasti s vysokou hustotou
    high_density_areas = sum(1 for count in grid.values() if count > 5)
    return high_density_areas >= 3

def parse_input(filename: str) -> List[Robot]:
    robots = []
    with open(filename, 'r') as f:
        for line in f:
            pos, vel = line.strip().split()
            x, y = map(int, pos[2:].split(','))
            vx, vy = map(int, vel[2:].split(','))
            robots.append(Robot(x, y, vx, vy))
    return robots

# Hlavní program
def main():
    robots = parse_input("Day_14/input_14.txt")
    print(f"Načteno {len(robots)} robotů")
    
    pattern_time = find_pattern_time(robots)
    if pattern_time >= 0:
        print(f"\nVzor nalezen v čase: {pattern_time}")
    else:
        print("\nVzor nebyl nalezen")

if __name__ == "__main__":
    main()