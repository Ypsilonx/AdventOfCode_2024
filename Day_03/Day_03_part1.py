import re

with open("Day_03/input_03.txt", "r") as file:
    data = file.read()

pattern = r"mul\((\d{1,3}),(\d{1,3})\)"

matches = re.findall(pattern, data)

total_sum = 0

for match in matches:
    num1 = int(match[0])
    num2 = int(match[1])
    result = num1 * num2
    total_sum += result

print(total_sum)
