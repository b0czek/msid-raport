import csv
import requests
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Add Geo-coordinates to CSV data.')
    parser.add_argument('input_csv', type=str, help='Input CSV file path')
    parser.add_argument('output_csv', type=str, help='Output CSV file path')
    parser.add_argument('api_key', type=str, help='Google API Key')
    args = parser.parse_args()

def get_coordinates(address, api_key):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': api_key}
    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None, None

def process_csv(input_file, output_file, api_key):
    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['latitude', 'longitude']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            address = row['address']
            if 'Wrocław' not in address:
                address += ', Wrocław'
            lat, lng = get_coordinates(address, api_key)
            if lat is not None and lng is not None:
                row.update({'latitude': lat, 'longitude': lng})
                writer.writerow(row)
            else:
                print(f"Failed to get coordinates for: {row}")

def main():
    args = parse_arguments()

    process_csv(args.input_csv, args.output_csv, args.api_key)


if __name__ == "__main__": 
    main()