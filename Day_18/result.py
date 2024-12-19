from Day_18 import solve_memory_escape

# Pro plnou úlohu
with open('Day_18/input_18.txt', 'r') as f:
    input_data = f.read()
    result = solve_memory_escape(input_data, grid_size=71)
    print(f"Výsledek: {result}")