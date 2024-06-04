import argparse
import os
import json

rooms_dict = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

PARAM_VALUES = {
    "furniture": lambda x: x['key'] == "yes",
    "price": lambda x: x['value'],
    "builttype": lambda x: x['key'],
    "m": lambda x: float(x['key']),
    "rooms": lambda x: rooms_dict[x['key']],
    "rent": lambda x: float(x['key']),
    "floor_select": lambda x: int(x['key'][6:]), # remove 'floor_' prefix

}


def parse_arguments():
    parser = argparse.ArgumentParser(description='Merge OLX API JSON files from scraper and extract basic data.')
    parser.add_argument('directory', type=str, help='The directory containing JSON files')
    parser.add_argument('output', type=str, help='The output file name')
    return parser.parse_args()

def process_offer(data):
    offer = {
        'id': data['id'],
        'title': data['title'],
        'description':  data['description'],
    }

    for param in data['params']:
        offer[param['key']] = PARAM_VALUES[param['key']](param['value'])

    return offer

def process_json_file(file_path, output_dict):
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            for item in data:
                if item['id'] not in output_dict:
                    output_dict[item['id']] = process_offer(item)

        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {file_path}")

def process_json_files(directory):
    unique_data = {}
    for file_name in os.listdir(directory):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory, file_name)
            process_json_file(file_path, unique_data)

    return list(unique_data.values())

def save_to_file(output_file, data):
    with open(output_file, 'w') as file:
        json.dump(data, file, separators=(',', ':'))

def main():
    args = parse_arguments()
    unique_data = process_json_files(args.directory)
    save_to_file(args.output, unique_data)

if __name__ == "__main__":
    main()
