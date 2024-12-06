#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <array>  // Přidáno pro std::array
#include <fstream>
#include <chrono>
#include <filesystem>
#include <bitset>
#include <unordered_set>

struct State {
    int16_t y;
    int16_t x;
    int8_t dir;

    bool operator==(const State& other) const {
        return y == other.y && x == other.x && dir == other.dir;
    }
};

struct StateHash {
    std::size_t operator()(const State& s) const {
        return (static_cast<size_t>(s.y) << 32) | 
               (static_cast<size_t>(s.x) << 16) | 
               static_cast<size_t>(s.dir);
    }
};

class GuardMovement {
private:
    std::vector<uint8_t> map;
    int height;
    int width;
    const std::array<std::pair<int8_t, int8_t>, 4> directions{{
        {-1, 0}, {0, 1}, {1, 0}, {0, -1}
    }};  // Upravená inicializace array
    State initial_state;

    inline bool is_valid_position(int y, int x) const {
        return static_cast<unsigned>(y) < static_cast<unsigned>(height) && 
               static_cast<unsigned>(x) < static_cast<unsigned>(width);
    }

    inline uint8_t& at(int y, int x) {
        return map[y * width + x];
    }

    inline const uint8_t& at(int y, int x) const {
        return map[y * width + x];
    }

    bool detect_loop(int obstacle_y, int obstacle_x) {
        std::vector<uint8_t> temp_map = map;
        temp_map[obstacle_y * width + obstacle_x] = 2;

        State current = initial_state;
        std::unordered_set<State, StateHash> visited;

        for (int steps = 0; steps < 1000; ++steps) {
            if (!visited.insert(current).second) {
                return true;
            }

            int next_y = current.y + directions[current.dir].first;
            int next_x = current.x + directions[current.dir].second;

            if (!is_valid_position(next_y, next_x)) {
                return false;
            }

            if (temp_map[next_y * width + next_x] > 0) {
                current.dir = (current.dir + 1) & 3;
            } else {
                current.y = next_y;
                current.x = next_x;
            }
        }
        return false;
    }

public:
    GuardMovement(const std::vector<std::string>& map_data) {
        height = map_data.size();
        width = map_data[0].length();
        map.resize(height * width);

        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                char c = map_data[y][x];
                if (c == '#') {
                    at(y, x) = 1;
                } else if (c == '^') {
                    initial_state = {static_cast<int16_t>(y), static_cast<int16_t>(x), 0};
                } else if (c == '>') {
                    initial_state = {static_cast<int16_t>(y), static_cast<int16_t>(x), 1};
                } else if (c == 'v') {
                    initial_state = {static_cast<int16_t>(y), static_cast<int16_t>(x), 2};
                } else if (c == '<') {
                    initial_state = {static_cast<int16_t>(y), static_cast<int16_t>(x), 3};
                }
            }
        }
    }

    int find_loop_positions() {
        int loop_count = 0;
        auto start_time = std::chrono::steady_clock::now();
        int processed = 0;
        int total = height * width;

        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                if (at(y, x) == 0 && (y != initial_state.y || x != initial_state.x)) {
                    if (detect_loop(y, x)) {
                        loop_count++;
                    }
                }
                
                processed++;
                if (processed % 100 == 0 || processed == total) {
                    auto current_time = std::chrono::steady_clock::now();
                    auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(current_time - start_time).count();
                    double progress = static_cast<double>(processed) / total * 100;
                    std::cout << "\rProgress: " << std::fixed << std::setprecision(1) 
                            << progress << "% Loops found: " << loop_count 
                            << " Time: " << elapsed << "s" << std::flush;
                }
            }
        }

        auto end_time = std::chrono::steady_clock::now();
        auto total_time = std::chrono::duration_cast<std::chrono::seconds>(end_time - start_time).count();
        std::cout << "\nCompleted in " << total_time << " seconds\n";
        return loop_count;
    }
};

int main() {
    std::vector<std::string> test_input = {
        "....#.....",
        ".........#",
        "..........",
        "..#.......",
        ".......#..",
        "..........",
        ".#..^.....",
        "........#.",
        "#.........",
        "......#..."
    };
    
    std::cout << "Testing with sample data...\n";
    GuardMovement test_guard(test_input);
    int test_result = test_guard.find_loop_positions();
    std::cout << "Test result: " << test_result << " (should be 6)\n\n";
    
    std::cout << "Processing input file...\n";
    const std::string filename = "D:/61_Programing/AOC/AdventOfCode_2024/Day_06/input_06.txt";
    
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Could not open file: " << filename << std::endl;
        return 1;
    }

    std::vector<std::string> input_data;
    std::string line;
    while (std::getline(file, line)) {
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        input_data.push_back(line);
    }

    if (!input_data.empty()) {
        GuardMovement guard(input_data);
        int result = guard.find_loop_positions();
        std::cout << "\nFINAL RESULT: " << result << std::endl;
    } else {
        std::cout << "Failed to load input data" << std::endl;
    }
    
    return 0;
}