#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <algorithm>

using namespace std;

struct FileInfo {
    int id;
    size_t start;
    size_t size;
};

vector<int> parseDiskMap(const string& diskMap) {
    vector<int> result;
    result.reserve(diskMap.length());
    for (char c : diskMap) {
        result.push_back(c - '0');
    }
    return result;
}

vector<FileInfo> findFiles(const vector<int>& blocks) {
    vector<FileInfo> files;
    files.reserve(blocks.size() / 2);  // Přibližná rezervace
    
    int currentFile = -1;
    size_t currentStart = 0;
    size_t currentSize = 0;

    for (size_t i = 0; i <= blocks.size(); i++) {
        if (i == blocks.size() || blocks[i] == -1 || (currentFile != -1 && blocks[i] != currentFile)) {
            if (currentFile != -1) {
                files.push_back({currentFile, currentStart, currentSize});
            }
            if (i < blocks.size() && blocks[i] != -1) {
                currentFile = blocks[i];
                currentStart = i;
                currentSize = 1;
            } else {
                currentFile = -1;
            }
        } else if (blocks[i] != -1) {
            if (currentFile == -1) {
                currentFile = blocks[i];
                currentStart = i;
                currentSize = 1;
            } else {
                currentSize++;
            }
        }
    }

    sort(files.begin(), files.end(), 
         [](const FileInfo& a, const FileInfo& b) { return a.id > b.id; });
    return files;
}

inline size_t findFreeSpace(const vector<int>& blocks, size_t size, size_t maxPosition) {
    size_t consecutiveSpace = 0;
    size_t spaceStart = 0;

    for (size_t i = 0; i < maxPosition; i++) {
        if (blocks[i] == -1) {
            if (consecutiveSpace == 0) spaceStart = i;
            if (++consecutiveSpace >= size) return spaceStart;
        } else {
            consecutiveSpace = 0;
        }
    }
    return maxPosition;
}

vector<int> createBlockRepresentation(const vector<int>& sizes) {
    vector<int> blocks;
    size_t totalSize = 0;
    for (size_t i = 0; i < sizes.size(); i++) {
        totalSize += sizes[i];
    }
    blocks.reserve(totalSize);
    
    int fileId = 0;
    for (size_t i = 0; i < sizes.size(); ++i) {
        if (i % 2 == 0) {
            blocks.insert(blocks.end(), sizes[i], fileId++);
        } else {
            blocks.insert(blocks.end(), sizes[i], -1);
        }
    }
    return blocks;
}

inline void moveFile(vector<int>& blocks, const FileInfo& file, size_t newPosition) {
    fill(blocks.begin() + newPosition, blocks.begin() + newPosition + file.size, file.id);
    fill(blocks.begin() + file.start, blocks.begin() + file.start + file.size, -1);
}

long long calculateChecksum(const vector<int>& blocks) {
    long long checksum = 0;
    for (size_t i = 0; i < blocks.size(); i++) {
        if (blocks[i] != -1) {
            checksum += (long long)i * blocks[i];
        }
    }
    return checksum;
}

long long solveDiskDefragPart2(const string& diskMap) {
    auto sizes = parseDiskMap(diskMap);
    auto blocks = createBlockRepresentation(sizes);
    auto files = findFiles(blocks);
    
    for (const auto& file : files) {
        size_t newPos = findFreeSpace(blocks, file.size, file.start);
        if (newPos < file.start) {
            moveFile(blocks, file, newPos);
        }
    }

    return calculateChecksum(blocks);
}

int main() {
    ifstream file("Day_09/input_09.txt");
    string inputData;
    getline(file, inputData);
    
    auto start = chrono::high_resolution_clock::now();
    long long result = solveDiskDefragPart2(inputData);
    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    
    cout << "Vysledek: " << result << endl;
    cout << "Cas: " << duration.count() << "ms" << endl;
    
    return 0;
}