def validace(sekvence_stranek, pravidla):
    rule_dict = {}
    for rule in pravidla:
        a, b = map(int, rule.strip().split('|'))
        if a not in rule_dict:
            rule_dict[a] = []
        rule_dict[a].append(b)
    
    for i, num in enumerate(sekvence_stranek):
        if num in rule_dict:
            required_numbers = rule_dict[num]
            remaining_sequence = sekvence_stranek[i+1:]
            for required_num in required_numbers:
                if required_num in sekvence_stranek and required_num not in remaining_sequence:
                    print(f"Rule violated: {num}|{required_num} - {required_num} must appear after {num}")
                    return False
    return True

def find_middle_number(sekvence_stranek):
    return sekvence_stranek[len(sekvence_stranek) // 2]

def process_sekvence(obsah):
    pravidla = []
    sekvence = []
    
    for line in obsah.split('\n'):
        line = line.strip()
        if not line:
            continue
        if '|' in line:
            pravidla.append(line)
        else:
            try:
                seq = [int(x) for x in line.split(',')]
                sekvence.append(seq)
            except:
                continue

    valid_sekvence = []
    prostredni_cislo = []
    
    for i, seq in enumerate(sekvence, 1):
        result = validace(seq, pravidla)
        if result:
            valid_sekvence.append(seq)
            prostredni_cislo.append(find_middle_number(seq))
            print(f"Sekvence {i}: {seq}")
            print(f"Prostřední číslo: {prostredni_cislo[-1]}")
            print()
    
    print(f"Celkem platných sekvencí: {len(valid_sekvence)}")
    print(f"Součet prostředních čísel: {sum(prostredni_cislo)}")
    return valid_sekvence, prostredni_cislo

# Načtení souboru a spuštění validace
with open('Day_05/input_05.txt', 'r') as file:
    obsah = file.read()
    valid_seqs, middle_nums = process_sekvence(obsah)

# _____________________________________________________________________________________________
# PART 2:
    
def create_graph(pravidla):
    graph = {}
    for rule in pravidla:
        a, b = map(int, rule.strip().split('|'))
        if a not in graph:
            graph[a] = set()
        graph[a].add(b)
    return graph

def topological_sort(sekvence_stranek, pravidla):
    graph = create_graph(pravidla)
    sequence_set = set(sekvence_stranek)
    
    in_degree = {num: 0 for num in sekvence_stranek}
    for node in graph:
        if node in sequence_set:
            for neighbor in graph[node]:
                if neighbor in sequence_set:
                    in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
    
    queue = [num for num in sekvence_stranek if in_degree[num] == 0]
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
        obsah = file.read()
    
    pravidla = []
    sekvence = []
    for line in obsah.split('\n'):
        line = line.strip()
        if not line:
            continue
        if '|' in line:
            pravidla.append(line)
        else:
            try:
                seq = [int(x) for x in line.split(',')]
                sekvence.append(seq)
            except:
                continue
    
    invalid_sekvence = []
    for seq in sekvence:
        if not validace(seq, pravidla):
            invalid_sekvence.append(seq)
    
    corrected_sekvence = []
    prostredni_cislo = []
    for seq in invalid_sekvence:
        corrected = topological_sort(seq, pravidla)
        if corrected:
            corrected_sekvence.append(corrected)
            prostredni_cislo.append(corrected[len(corrected)//2])
            print(f"Původní sekvence: {seq}")
            print(f"Opravená sekvence: {corrected}")
            print(f"Prostřední číslo: {corrected[len(corrected)//2]}\n")
    
    print(f"Součet prostředních čísel opravených sekvencí: {sum(prostredni_cislo)}")
    return corrected_sekvence, prostredni_cislo

# Spuštění
corrected_seqs, middle_nums = process_file('Day_05/input_05.txt')