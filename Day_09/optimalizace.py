from array import array

def parse_disk_map(disk_map: str) -> list:
    """Převede řetězec mapy disku na seznam bloků s jejich velikostmi."""
    return [int(x) for x in str(disk_map).strip()]

def create_block_representation(sizes: list) -> array:
    """Vytvoří reprezentaci bloků, kde každý blok je označen ID souboru nebo -1 pro volné místo."""
    blocks = array('i')
    file_id = 0
    for i, size in enumerate(sizes):
        if i % 2 == 0:
            blocks.extend([file_id] * size)
            file_id += 1
        else:
            blocks.extend([-1] * size)
    return blocks

def move_file_left(blocks: array) -> bool:
    """Pokusí se přesunout jeden soubor zleva doprava."""
    last_file = None
    last_file_start = -1
    
    for i in range(len(blocks)-1, -1, -1):
        if blocks[i] != -1:
            if last_file is None:
                last_file = blocks[i]
                last_file_start = i
            elif blocks[i] != last_file:
                break
    
    if last_file is None:
        return False
    
    try:
        first_space = blocks.index(-1)
    except ValueError:
        return False
    
    if first_space >= last_file_start:
        return False
    
    file_size = 0
    for i in range(last_file_start, len(blocks)):
        if blocks[i] == last_file:
            file_size += 1
        else:
            break
    
    for i in range(last_file_start, last_file_start + file_size):
        blocks[i] = -1
    for i in range(first_space, first_space + file_size):
        blocks[i] = last_file
    
    return True

def calculate_checksum(blocks: array) -> int:
    """Vypočítá kontrolní součet podle zadaných pravidel."""
    return sum(pos * block for pos, block in enumerate(blocks) if block != -1)

def solve_disk_defrag(disk_map: str) -> int:
    """Hlavní funkce řešení."""
    sizes = parse_disk_map(disk_map)
    blocks = create_block_representation(sizes)
    
    while move_file_left(blocks):
        pass
    
    return calculate_checksum(blocks)

def print_blocks(blocks):
    """Vytiskne reprezentaci bloků pro debugging."""
    print(''.join(str(x) if x != -1 else '.' for x in blocks))

if __name__ == "__main__":
    test_input = "2333133121414131402"
    test_result = solve_disk_defrag(test_input)
    print(f"Test kontrolní součet: {test_result}")
    
    with open("Day_09/input_09.txt", "r") as file:
        input_data = file.read().strip()
    
    result = solve_disk_defrag(input_data)
    print(f"Výsledný kontrolní součet: {result}")