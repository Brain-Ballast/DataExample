#!/usr/bin/env python3
import re
import sys

def filter_file(input_file, output_file=None):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        filtered_lines = []
        removed_length = 0
        removed_range = 0
        removed_letters = 0
        
        pattern = re.compile(r'[a-zA-Z:]')
        
        for line in lines:
            line_content = line.rstrip('\n\r')
            
            if not (33 <= len(line_content) <= 40):
                removed_length += 1
                continue
            
            if line_content.strip():
                try:
                    first_value = line_content.split(',')[0].strip()
                    first_number = float(first_value)
                    
                    if not (0.0 <= first_number <= 4000):
                        removed_range += 1
                        continue
                        
                except (ValueError, IndexError):
                    removed_range += 1
                    continue
            
            if pattern.search(line_content):
                removed_letters += 1
                continue
            
            filtered_lines.append(line)
        
        if output_file is None:
            output_file = input_file
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(filtered_lines)
        
        print(f"Lines kept: {len(filtered_lines)}")
        print(f"Removed by length: {removed_length}")
        print(f"Removed by range: {removed_range}")
        print(f"Removed by letters/colons: {removed_letters}")
        print(f"Total removed: {removed_length + removed_range + removed_letters}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    filter_file(input_file, output_file)