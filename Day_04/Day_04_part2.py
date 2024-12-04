def find_all_diagonal_patterns(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = [['.' for _ in range(cols)] for _ in range(rows)]
    count = 0
    
    patterns = [
        {'center': 'A',
         'top_left': 'M', 'top_right': 'S',
         'bottom_left': 'M', 'bottom_right': 'S'},
        {'center': 'A',
         'top_left': 'S', 'top_right': 'M',
         'bottom_left': 'S', 'bottom_right': 'M'},
        {'center': 'A',
         'top_left': 'S', 'top_right': 'S',
         'bottom_left': 'M', 'bottom_right': 'M'},
        {'center': 'A',
         'top_left': 'M', 'top_right': 'M',
         'bottom_left': 'S', 'bottom_right': 'S'}
    ]
    
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            for pattern in patterns:
                if (matrix[i][j] == pattern['center'] and
                    matrix[i-1][j-1] == pattern['top_left'] and 
                    matrix[i-1][j+1] == pattern['top_right'] and
                    matrix[i+1][j-1] == pattern['bottom_left'] and 
                    matrix[i+1][j+1] == pattern['bottom_right']):
                    
                    result[i][j] = pattern['center']
                    result[i-1][j-1] = pattern['top_left']
                    result[i-1][j+1] = pattern['top_right']
                    result[i+1][j-1] = pattern['bottom_left']
                    result[i+1][j+1] = pattern['bottom_right']
                    count += 1
    
    return result, count

def process_large_file(input_filename, output_filename):
    try:
        print("Načítám soubor...")
        with open(input_filename, 'r') as file:
            matrix = [list(line.strip()) for line in file if line.strip()]
        
        if not matrix or not all(len(row) == len(matrix[0]) for row in matrix):
            raise ValueError("Nevalidní formát matice v souboru")
            
        print(f"Načtena matice o velikosti {len(matrix)}x{len(matrix[0])}")
        
        print("Hledám vzory...")
        result_matrix, count = find_all_diagonal_patterns(matrix)
        
        print("Zapisuji výsledky...")
        with open(output_filename, 'w') as file:
            file.write(f"Nalezeno {count} výskytů vzoru\n\n")
            file.write("Výsledná matice:\n")
            for row in result_matrix:
                file.write(''.join(row) + '\n')
        
        print(f"Hotovo! Nalezeno {count} výskytů.")
        print(f"Výsledky byly zapsány do souboru: {output_filename}")
        
    except FileNotFoundError:
        print(f"Chyba: Soubor {input_filename} nebyl nalezen")
    except Exception as e:
        print(f"Chyba při zpracování: {str(e)}")

if __name__ == "__main__":
    input_file = "Day_04/input_04.txt"  # název vstupního souboru
    output_file = "Day_04/output_04.txt"  # název výstupního souboru
    process_large_file(input_file, output_file)