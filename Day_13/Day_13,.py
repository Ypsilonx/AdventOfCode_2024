from typing import Tuple, Optional
from math import gcd

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Rozšířený Euklidův algoritmus pro nalezení řešení ax + by = gcd(a,b)
    Vrací (gcd, x, y)
    """
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def solve_system(button_a: Tuple[int, int], button_b: Tuple[int, int], 
                target: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    """
    Řeší soustavu dvou lineárních diofantických rovnic:
    ax * A + bx * B = target_x
    ay * A + by * B = target_y
    
    Vrací nejlevnější nezáporné řešení (počet stisknutí A, počet stisknutí B)
    nebo None pokud řešení neexistuje.
    """
    ax, ay = button_a
    bx, by = button_b
    tx, ty = target
    
    coef = ay*bx - ax*by
    if coef == 0:  
        return None
        
    right_side = ay*tx - ax*ty
    
    if right_side % coef != 0: 
        return None
        
    B = right_side // coef
    
    if ax != 0:
        A = (tx - bx*B) // ax
    else:
        A = (ty - by*B) // ay
        
    if A < 0 or B < 0:
        return None
        
    if (A*ax + B*bx == tx) and (A*ay + B*by == ty):
        return (A, B)
        
    return None

def parse_input(text: str, add_large_number: bool = False) -> list[tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
    """Zpracuje vstupní text na seznam trojic (tlačítko A, tlačítko B, cíl)"""
    machines = []
    current_machine = []
    large_number = 10**13 if add_large_number else 0
    
    for line in text.strip().split('\n'):
        if not line:
            continue
            
        if line.startswith('Button A:'):
            parts = line.split(',')
            x = int(parts[0].split('+')[1])
            y = int(parts[1].split('+')[1])
            current_machine.append((x, y))
        elif line.startswith('Button B:'):
            parts = line.split(',')
            x = int(parts[0].split('+')[1])
            y = int(parts[1].split('+')[1])
            current_machine.append((x, y))
        elif line.startswith('Prize:'):
            parts = line.split(',')
            x = int(parts[0].split('=')[1]) + large_number
            y = int(parts[1].split('=')[1]) + large_number
            current_machine.append((x, y))
            machines.append(tuple(current_machine))
            current_machine = []
            
    return machines

def calculate_total_cost(machines: list, part: int) -> int:
    """Spočítá celkovou minimální cenu pro všechny řešitelné automaty"""
    total_cost = 0
    solvable_count = 0
    
    print(f"\nČást {part}:")
    for i, (button_a, button_b, target) in enumerate(machines, 1):
        solution = solve_system(button_a, button_b, target)
        if solution:
            a_presses, b_presses = solution
            cost = a_presses * 3 + b_presses * 1
            total_cost += cost
            solvable_count += 1
            print(f"Automat {i}: Řešitelný - A: {a_presses}x, B: {b_presses}x, Cena: {cost} tokenů")
        else:
            print(f"Automat {i}: Neřešitelný")
    
    print(f"\nCelkem řešitelných automatů: {solvable_count}")
    print(f"Celková minimální cena: {total_cost} tokenů")
    return total_cost

def main():
    try:
        with open('Day_13/input_13.txt', 'r') as file:
            input_data = file.read()
        
        machines = parse_input(input_data, add_large_number=False)
        result1 = calculate_total_cost(machines, 1)
        
        machines = parse_input(input_data, add_large_number=True)
        result2 = calculate_total_cost(machines, 2)
        
    except FileNotFoundError:
        print("Soubor 'input_13.txt' nebyl nalezen!")
    except Exception as e:
        print(f"Nastala chyba při zpracování souboru: {e}")

if __name__ == "__main__":
    main()