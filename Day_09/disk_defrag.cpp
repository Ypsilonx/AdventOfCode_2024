#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>

using namespace std;

vector<int> parseDiskMap(const string& diskMap) {
    vector<int> result;
    result.reserve(diskMap.length());
    for (char c : diskMap) {
        result.push_back(c - '0');
    }
    return result;
}

vector<int> createBlockRepresentation(const vector<int>& sizes) {
    vector<int> blocks;
    blocks.reserve(sizes.size() * 9); 
    int fileId = 0;
    
    for (size_t i = 0; i < sizes.size(); ++i) {
        if (i % 2 == 0) { // soubor
            blocks.insert(blocks.end(), sizes[i], fileId++);
        } else { // volné místo
            blocks.insert(blocks.end(), sizes[i], -1);
        }
    }
    return blocks;
}

bool moveFileLeft(vector<int>& blocks) {
    int lastFile = -1;
    int lastFileStart = -1;
    
    for (int i = blocks.size() - 1; i >= 0; --i) {
        if (blocks[i] != -1) {
            if (lastFile == -1) {
                lastFile = blocks[i];
                lastFileStart = i;
            } else if (blocks[i] != lastFile) {
                break;
            }
        }
    }
    
    if (lastFile == -1) return false;
    
    int firstSpace = -1;
    for (size_t i = 0; i < blocks.size(); ++i) {
        if (blocks[i] == -1) {
            firstSpace = i;
            break;
        }
    }
    
    if (firstSpace == -1 || firstSpace >= lastFileStart) return false;
    
    int fileSize = 0;
    for (size_t i = lastFileStart; i < blocks.size() && blocks[i] == lastFile; ++i) {
        fileSize++;
    }
    
    fill(blocks.begin() + lastFileStart, blocks.begin() + lastFileStart + fileSize, -1);
    fill(blocks.begin() + firstSpace, blocks.begin() + firstSpace + fileSize, lastFile);
    
    return true;
}

long long calculateChecksum(const vector<int>& blocks) {
    long long checksum = 0;
    for (size_t i = 0; i < blocks.size(); ++i) {
        if (blocks[i] != -1) {
            checksum += i * blocks[i];
        }
    }
    return checksum;
}

long long solveDiskDefrag(const string& diskMap) {
    auto sizes = parseDiskMap(diskMap);
    auto blocks = createBlockRepresentation(sizes);
    
    while (moveFileLeft(blocks)) {}
    
    return calculateChecksum(blocks);
}

void printBlocks(const vector<int>& blocks) {
    for (int block : blocks) {
        if (block == -1) cout << '.';
        else cout << block;
    }
    cout << endl;
}

int main() {
    string testInput = "2333133121414131402";
    auto start = chrono::high_resolution_clock::now();
    long long testResult = solveDiskDefrag(testInput);
    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    
    cout << "Test kontrolni soucet: " << testResult << endl;
    cout << "Test cas: " << duration.count() << "ms" << endl;
    
    ifstream file("Day_09/input_09.txt");
    string inputData;
    getline(file, inputData);
    
    start = chrono::high_resolution_clock::now();
    long long result = solveDiskDefrag(inputData);
    end = chrono::high_resolution_clock::now();
    duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    
    cout << "Vysledny kontrolni soucet: " << result << endl;
    cout << "Cas zpracovani: " << duration.count() << "ms" << endl;
    
    return 0;
}