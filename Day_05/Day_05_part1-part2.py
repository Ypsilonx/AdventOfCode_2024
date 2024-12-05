def validate_sequence(sequence, rules):
    rule_dict = {}
    for rule in rules:
        a, b = map(int, rule.strip().split('|'))
        if a not in rule_dict:
            rule_dict[a] = []
        rule_dict[a].append(b)
    
    for i, num in enumerate(sequence):
        if num in rule_dict:
            required_numbers = rule_dict[num]
            remaining_sequence = sequence[i+1:]
            for required_num in required_numbers:
                if required_num in sequence and required_num not in remaining_sequence:
                    print(f"Rule violated: {num}|{required_num} - {required_num} must appear after {num}")
                    return False
    return True

def find_middle_number(sequence):
    return sequence[len(sequence) // 2]

def process_sequences(content):
    rules = []
    sequences = []
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if '|' in line:
            rules.append(line)
        else:
            try:
                seq = [int(x) for x in line.split(',')]
                sequences.append(seq)
            except:
                continue

    valid_sequences = []
    middle_numbers = []
    
    for i, seq in enumerate(sequences, 1):
        result = validate_sequence(seq, rules)
        if result:
            valid_sequences.append(seq)
            middle_numbers.append(find_middle_number(seq))
            print(f"Sekvence {i}: {seq}")
            print(f"Prostřední číslo: {middle_numbers[-1]}")
            print()
    
    print(f"Celkem platných sekvencí: {len(valid_sequences)}")
    print(f"Součet prostředních čísel: {sum(middle_numbers)}")
    return valid_sequences, middle_numbers

# Načtení souboru a spuštění validace
with open('Day_05/input_05.txt', 'r') as file:
    content = file.read()
    valid_seqs, middle_nums = process_sequences(content)

# _____________________________________________________________________________________________

    
def create_graph(rules):
    graph = {}
    for rule in rules:
        a, b = map(int, rule.strip().split('|'))
        if a not in graph:
            graph[a] = set()
        graph[a].add(b)
    return graph

def topological_sort(sequence, rules):
    graph = create_graph(rules)
    # Vytvoření množiny čísel v sekvenci
    sequence_set = set(sequence)
    
    # Inicializace vstupních stupňů
    in_degree = {num: 0 for num in sequence}
    for node in graph:
        if node in sequence_set:
            for neighbor in graph[node]:
                if neighbor in sequence_set:
                    in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
    
    # Nalezení všech vrcholů s nulovým vstupním stupněm
    queue = [num for num in sequence if in_degree[num] == 0]
    result = []
    
    while queue:
        node = queue.pop(0)
        result.append(node)
        
        if node in graph:
            for neighbor in graph[node]:
                if neighbor in sequence_set:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)
    
    return result

def process_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    
    rules = []
    sequences = []
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if '|' in line:
            rules.append(line)
        else:
            try:
                seq = [int(x) for x in line.split(',')]
                sequences.append(seq)
            except:
                continue
    
    invalid_sequences = []
    for seq in sequences:
        if not validate_sequence(seq, rules):
            invalid_sequences.append(seq)
    
    corrected_sequences = []
    middle_numbers = []
    for seq in invalid_sequences:
        corrected = topological_sort(seq, rules)
        if corrected:
            corrected_sequences.append(corrected)
            middle_numbers.append(corrected[len(corrected)//2])
            print(f"Původní sekvence: {seq}")
            print(f"Opravená sekvence: {corrected}")
            print(f"Prostřední číslo: {corrected[len(corrected)//2]}\n")
    
    print(f"Součet prostředních čísel opravených sekvencí: {sum(middle_numbers)}")
    return corrected_sequences, middle_numbers

# Spuštění
corrected_seqs, middle_nums = process_file('Day_05/input_05.txt')