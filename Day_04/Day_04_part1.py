def find_xmas(grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    word = "XMAS"
    word_len = len(word)
    count = 0

    def is_valid(x, y):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def search_from(x, y, dx, dy):
        for k in range(word_len):
            nx, ny = x + k * dx, y + k * dy
            if not is_valid(nx, ny) or grid[nx][ny] != word[k]:
                return False
        return True

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'X':
                for dx, dy in directions:
                    if search_from(i, j, dx, dy):
                        count += 1
    return count

def read_grid_from_file(filename):
    with open(filename, 'r') as file:
        grid = [list(line.strip()) for line in file]
    return grid

filename = 'Day_04/input_04.txt'
grid = read_grid_from_file(filename)

xmas_count = find_xmas(grid)
print(f"Počet XMAS: {xmas_count}")
