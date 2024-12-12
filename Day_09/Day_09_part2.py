from dataclasses import dataclass
from typing import List, Tuple
import time

@dataclass
class FileInfo:
    id: int
    start: int
    size: int

def parse_disk_map(disk_map: str) -> List[int]:
    """Převede vstupní string na list čísel."""
    return [int(x) for x in disk_map.strip()]

def find_files(blocks: List[int]) -> List[FileInfo]:
    """Najde všechny soubory a jejich pozice."""
    files = []
    current_file = -1
    current_start = 0
    current_size = 0
    
    for i, block in enumerate(blocks + [-1]):  # Přidáme -1 na konec pro zpracování posledního souboru
        if block == -1 or (current_file != -1 and block != current_file):
            if current_file != -1:
                files.append(FileInfo(current_file, current_start, current_size))
            if block != -1:
                current_file = block
                current_start = i
                current_size = 1
            else:
                current_file = -1
        elif block != -1:
            if current_file == -1:
                current_file = block
                current_start = i
                current_size = 1
            else:
                current_size += 1
    
    # Seřadit podle ID sestupně
    return sorted(files, key=lambda x: x.id, reverse=True)

def find_free_space(blocks: List[int], size: int, max_position: int) -> int:
    """Najde první dostatečně velký volný prostor."""
    consecutive_space = 0
    space_start = 0
    
    for i in range(max_position):
        if blocks[i] == -1:
            if consecutive_space == 0:
                space_start = i
            consecutive_space += 1
            if consecutive_space >= size:
                return space_start
        else:
            consecutive_space = 0
    
    return max_position

def create_block_representation(sizes: List[int]) -> List[int]:
    """Vytvoří reprezentaci bloků z velikostí."""
    blocks = []
    file_id = 0
    
    for i, size in enumerate(sizes):
        if i % 2 == 0:  # soubor
            blocks.extend([file_id] * size)
            file_id += 1
        else:  # mezera
            blocks.extend([-1] * size)
    
    return blocks

def move_file(blocks: List[int], file: FileInfo, new_position: int):
    """Přesune soubor na novou pozici."""
    # Zapíše soubor na novou pozici
    blocks[new_position:new_position + file.size] = [file.id] * file.size
    # Vymaže původní pozici
    blocks[file.start:file.start + file.size] = [-1] * file.size

def calculate_checksum(blocks: List[int]) -> int:
    """Vypočítá kontrolní součet."""
    return sum(i * block for i, block in enumerate(blocks) if block != -1)

def solve_disk_defrag_part2(disk_map: str) -> int:
    """Hlavní funkce řešení."""
    # Parse vstup
    sizes = parse_disk_map(disk_map)
    blocks = create_block_representation(sizes)
    
    # Najdi soubory
    files = find_files(blocks)
    
    # Pro každý soubor od nejvyššího ID
    for file in files:
        # Najdi první vhodný volný prostor vlevo
        new_pos = find_free_space(blocks, file.size, file.start)
        # Pokud byl nalezen vhodný prostor a je vlevo od současné pozice
        if new_pos < file.start:
            move_file(blocks, file, new_pos)
    
    return calculate_checksum(blocks)

if __name__ == "__main__":
    # Test na příkladu ze zadání
    test_input = "2333133121414131402"
    start_time = time.time()
    test_result = solve_disk_defrag_part2(test_input)
    print(f"Test kontrolní součet: {test_result}")  # Mělo by být 2858
    print(f"Test čas: {(time.time() - start_time)*1000:.2f}ms")
    
    # Načtení a zpracování skutečného vstupu
    with open("Day_09/input_09.txt", "r") as file:
        input_data = file.read().strip()
    
    start_time = time.time()
    result = solve_disk_defrag_part2(input_data)
    end_time = time.time()
    
    print(f"Výsledný kontrolní součet: {result}")
    print(f"Čas zpracování: {(end_time - start_time)*1000:.2f}ms")