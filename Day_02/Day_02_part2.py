with open('Day_02/input_02.txt', 'r') as file:
    lines = file.readlines()

data = []
for line in lines:
    numbers = list(map(int, line.strip().split()))
    data.append(numbers)

def is_valid_sequence(sequence):
    is_increasing = all(1 <= sequence[i+1] - sequence[i] <= 3 for i in range(len(sequence) - 1))
    is_decreasing = all(1 <= sequence[i] - sequence[i+1] <= 3 for i in range(len(sequence) - 1))
    return is_increasing or is_decreasing

def is_valid_after_removal(sequence):
    for i in range(len(sequence)):
        modified_sequence = sequence[:i] + sequence[i+1:]
        if is_valid_sequence(modified_sequence):
            return True
    return False

valid_sequences = [seq for seq in data if is_valid_sequence(seq)]
valid_strict_seq = [seq for seq in data if not is_valid_sequence(seq) and is_valid_after_removal(seq)]

print(len(valid_sequences))
print(len(valid_strict_seq))
