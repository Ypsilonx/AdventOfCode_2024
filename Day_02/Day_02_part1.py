with open('Day_02/input_02.txt', 'r') as file:
    lines = file.readlines()

data = []
for line in lines:
    numbers = list(map(int, line.strip().split()))
    data.append(numbers)

def is_valid_sequence(sequence):
    if all(sequence[i+1] > sequence[i] and 1 <= sequence[i+1] - sequence[i] <= 3 for i in range(len(sequence) - 1)):
        return True
    if all(sequence[i+1] < sequence[i] and 1 <= sequence[i] - sequence[i+1] <= 3 for i in range(len(sequence) - 1)):
        return True
    return False

valid_sequences = [seq for seq in data if is_valid_sequence(seq)]

print(len(valid_sequences))
