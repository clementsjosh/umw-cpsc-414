#!/usr/bin/python3

from collections import Counter

def count_first_strings(filename):
    """Counts the occurrences of the first string on each line of a file."""
    first_strings = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Ensure the line is not empty
                first_string = line.split()[0] # Split by whitespace and take the first element
                first_strings.append(first_string)
    
    return Counter(first_strings)


def count_second_strings(filename):
    """Counts the occurrences of the first string on each line of a file."""
    second_strings = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Ensure the line is not empty
                second_string = line.split()[0] # Split by whitespace and take the first element
                second_strings.append(second_string)
    
    return Counter(second_strings)

filename = "capture.pcap"
first_counts = count_first_strings(filename)
second_counts = count_second_strings(filename)
for string, count in first_counts.items():
    print(f"'{string}': {count} occurrences")
    
for string, count in second_counts.items():
    print(f"'{string}': {count} occurences")
