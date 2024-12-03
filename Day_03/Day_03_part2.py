import re
def process_section(section):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, section)
    total_sum = 0
    for match in matches:
        num1 = int(match[0])
        num2 = int(match[1])
        result = num1 * num2
        total_sum += result
    return total_sum

with open("Day_03/input_03.txt", "r") as file:
    data = file.read()

parts = re.split(r"(do\(\)|don't\(\))", data)

total_sum = 0
process = True

for part in parts:
    if part == "do()":
        process = True
    elif part == "don't()":
        process = False
    elif process:
        total_sum += process_section(part)

print("Celkový součet výsledků je:", total_sum)
