import json
import sys

def remove_duplicate_keys(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Process keys and values, retaining "like" over "dislike" if duplicates are found
    unique_data = {}
    for key, value in sorted(data.items(), key=lambda item: item[1], reverse=True):
        # Only add the key-value pair if the key is not already in unique_data
        # Since we're iterating through the sorted data, "like" values will be added first
        if key not in unique_data:
            unique_data[key] = value

    output_file = input_file.rsplit('.', 1)[0] + '-deduplicated.json'
    with open(output_file, 'w') as file:
        json.dump(unique_data, file, indent=4)

    print(f"Duplicates removed and saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.json>")
    else:
        input_file = sys.argv[1]
        remove_duplicate_keys(input_file)
