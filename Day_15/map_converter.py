def convert_map(input_map: str, output_file: str):
    """Převede původní mapu na rozšířenou verzi podle pravidel části 2"""
    with open(input_map, 'r') as f:
        lines = f.read().strip().split('\n')
    
    converted = []
    for line in lines:
        new_line = ''
        for char in line:
            if char == '#':
                new_line += '##'
            elif char == 'O':
                new_line += '[]'
            elif char == '.':
                new_line += '..'
            elif char == '@':
                new_line += '@.'
        converted.append(new_line)
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(converted))

if __name__ == "__main__":
    convert_map("Day_15/input_15.txt", "Day_15/warehouse_map.txt")